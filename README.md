# Advent of code
#### made easy


This repository is allows you to focus 100% on the task at hand, the daily puzzle. The rest is taken care by the repo.

In order to have all the functionality you need to use the package manager `poetry`, such that you can use the command aoc within the poetry shell.

```sh
aoc --help
```

will show you the basic commands it gives the users.

## aoc create

This command will scaffold up the days puzzle and a testing suite alongside it. If no day is provided, it will assume today.

## aoc remove

Removes the folder for the provided day. If no day is provided, it will assume today.

## aoc run

It will run the **live** puzzle input through your code and give you the answer. You need to provide a path to it in the `<day>:<level>` pattern.

## aoc test

It will test the **local** puzzle input through your code with the help of pytest. You need to provide a path to it in the `<day>:<level>` pattern.

## aoc submit

send your answer directly to `adventofcode.com` through the cli.

## aoc stats

check the stats for a particular day or part.
# Environment

In order for the cli to run through the **live** input data, it needs your session cookie. Create a `.env` file and store it in the root of this repository. You will find your sessionid by inspecting your network traffic sent to `adventofcode.com`
