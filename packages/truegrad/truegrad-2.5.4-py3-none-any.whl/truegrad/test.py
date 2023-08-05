import datetime
import torch
import optim
import time
from lion_pytorch import Lion
import copy
from matplotlib import pyplot as plt

numbers = 16
features = 2 ** 8
depth = 16
input_scale = 1
noise_scale = 0.01
lr = 0.1

a = torch.nn.Sequential(torch.nn.Linear(numbers, features), torch.nn.ReLU(), torch.nn.LayerNorm(features),
                        *[layer for _ in range(depth) for layer in [torch.nn.Linear(features, features), torch.nn.ReLU(), torch.nn.LayerNorm(features, features)]],
                        torch.nn.Linear(features, numbers)).cuda()
aa = [copy.deepcopy(a) for _ in range(3)]
oo = [torch.optim.Adam(aa[0].parameters(), lr=lr),
      optim.Graft(aa[1].parameters(), torch.optim.Adam(aa[1].parameters(), lr=lr), Lion(aa[1].parameters(), lr=1), weight_decay=0),
      optim.Graft(aa[2].parameters(), torch.optim.Adam(aa[2].parameters(), lr=lr), torch.optim.SGD(aa[2].parameters(), lr=1), weight_decay=0)]

all_losses = []
i = 0
while True:
    i += 1
    try:
        inp = torch.randn((1024, numbers), device="cuda:0") * input_scale
        noise = torch.randn((1024, numbers), device="cuda:0") * inp.std() * noise_scale
        losses = []
        for a, o in zip(aa, oo):
            out = (a(inp) - inp.square() + noise).abs().mean()
            out.backward()
            o.step()
            o.zero_grad()
            losses.append(out.item())
        all_losses.append(losses)
        if i % 128 == 0:
            print(f'{i:05d} | {datetime.datetime.now()} | {" - ".join(f"{o:10.6f}" for o in losses)}')
    except KeyboardInterrupt:
        break

skipped = len(all_losses) // 10
all_losses = all_losses[skipped:]
for name, ls in zip(["Adam#Adam", "Adam#Lion", "Adam#SGD", "Adam", "Lion", "SGD"], zip(*all_losses)):
    plt.plot(list(range(skipped, skipped + len(ls) - skipped)), [sum(ls[i:i+skipped]) / skipped for i in range(len(ls) - skipped)], label=name)
plt.yscale("log")
plt.xscale("log")
plt.legend()
plt.show()
