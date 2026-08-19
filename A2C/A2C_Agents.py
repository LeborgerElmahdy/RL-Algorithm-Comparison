import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import os
import config as cfg

class ActorCritic(nn.Module):
    def __init__(self, obs_dim=7, n_actions=cfg.NUM_ACTIONS, hidden=cfg.HIDDEN_SIZE):
        super().__init__()
        self.shared = nn.Sequential(
            nn.Linear(obs_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
        )
        self.policy_head = nn.Linear(hidden, n_actions)
        self.value_head = nn.Linear(hidden, 1)

    def forward(self, x):
        h = self.shared(x)
        return self.policy_head(h), self.value_head(h)


class A2CAgent:
    def __init__(self, obs_dim=7):
        self.net = ActorCritic(obs_dim=obs_dim)
        self.opt = optim.Adam(self.net.parameters(), lr=cfg.ACTOR_LR)
        self.gamma = cfg.GAMMA
        self._reset_buffer()

    def _reset_buffer(self):
        self.log_probs, self.values, self.rewards, self.entropies = [], [], [], []

    def select_action(self, state_vector):
        state_t = torch.from_numpy(state_vector).unsqueeze(0)
        logits, value = self.net(state_t)
        dist = torch.distributions.Categorical(logits=logits)
        action = dist.sample()

        self.log_probs.append(dist.log_prob(action).squeeze(0))
        self.values.append(value.squeeze())
        self.entropies.append(dist.entropy().squeeze(0))
        return action.item()

    def record_reward(self, reward):
        self.rewards.append(reward)

    def learn(self):
        if not self.rewards:
            return

        G, returns = 0.0, []
        for r in reversed(self.rewards):
            G = r + self.gamma * G
            returns.insert(0, G)
        returns = torch.tensor(returns, dtype=torch.float32)
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)

        values = torch.stack(self.values)
        log_probs = torch.stack(self.log_probs)
        entropies = torch.stack(self.entropies)

        advantages = returns - values.detach()
        actor_loss = -(log_probs * advantages).mean()
        critic_loss = F.mse_loss(values, returns)
        loss = actor_loss + cfg.VALUE_COEF * critic_loss - cfg.ENTROPY_COEF * entropies.mean()

        self.opt.zero_grad()
        loss.backward()
        self.opt.step()
        self._reset_buffer()
