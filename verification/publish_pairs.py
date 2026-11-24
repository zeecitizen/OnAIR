"""Verification helper for the fork only, not for upstream."""

import time

import redis

r1 = redis.Redis(host="localhost", port=6379)
r2 = redis.Redis(host="localhost", port=6380)


def publish(server, channel, n):
    server.publish(channel, '{"time":%d, "x":%s, "y":%s}' % (n, n + 0.1, n + 0.2))
    print("published", channel, n, flush=True)


# Part 1: one channel at a time, as in doc/redis-example.md
for n, (server, channel) in enumerate(
    [(r1, "state_0"), (r2, "state_1"), (r2, "state_2")]
):
    publish(server, channel, n)
    time.sleep(1)

# Part 2: two channels back to back, before OnAIR takes its next frame
for n in range(10, 210, 10):
    publish(r1, "state_0", n)
    publish(r2, "state_1", n + 1)
    time.sleep(0.5)
