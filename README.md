# python-awscli-local AUR Package

Seriously, I can't believe nobody bothered to maintain this on the AUR until now. 

If you're an Arch user trying to work with LocalStack and need the `awslocal` command, you've probably been through the same frustrating dance I did - manually installing it via pip, dealing with system/user Python conflicts, or just giving up and using Docker for everything.

Well, no more. This package is now properly maintained on the AUR and actually stays up to date automatically. Even though it has not been updated in years...

## What this is

This is the AUR package for [awscli-local](https://github.com/localstack/awscli-local) - that thin wrapper around the AWS CLI that lets you point commands at your local LocalStack instance instead of actual AWS.

You know, the thing that should have been packaged properly years ago when LocalStack became popular, but somehow wasn't.

## Installation

Finally, you can install it the proper Arch way:

```bash
# Using your favorite AUR helper
yay -S python-awscli-local

# Or manually
git clone https://aur.archlinux.org/python-awscli-local.git
cd python-awscli-local
makepkg -si
```

## Usage

After installation, you get the `awslocal` command:

```bash
# Instead of this mess:
aws --endpoint-url=http://localhost:4566 s3 ls

# Just do this:
awslocal s3 ls
```

You know, like it should be.

## Automatic Updates

Unlike apparently every other attempt at packaging this, this one actually stays up to date. There's a GitHub Actions workflow that checks PyPI daily and automatically updates the AUR package when new versions are released

## Why I Made This

Maintaining AUR packages isn't the most exciting thing in the world, I know. But when you're trying to develop against LocalStack on Arch and you have to jump through hoops just to get basic tooling installed, it gets old fast

So here we are. A properly maintained, automatically updated AUR package for `awscli-local` 

If you're reading this, you probably needed this too. You're welcome

## Contributing

The automation handles version updates, but if you notice any issues with the package itself, feel free to open an issue or PR. Or flag it out of date on the AUR

The workflow and scripts are all here in the repo if you want to see how the auto-updates work, or if you want to adapt this approach for your own AUR packages that nobody else is maintaining properly

## Links

- [AUR Package](https://aur.archlinux.org/packages/python-awscli-local)
- [Upstream Project](https://github.com/localstack/awscli-local)
- [LocalStack](https://github.com/localstack/localstack)

---

*Finally, a properly maintained awscli-local package for Arch users...*
