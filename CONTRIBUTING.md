# Contributing to reflective-potential

> This project has a [code of conduct][conduct]. By interacting with this 
> repository, organization, or community you agree to abide by its terms.

## Where to start?

*This project is currently in alpha testing while a manuscript describing its 
motivation, data, methods, and results is drafted for peer review.* We welcome 
contributions in the form of bug reports, bug fixes, code quality enhancements, 
documentation improvements, and scientific ideas.

Contributions are tracked as [GitHub issues][issue]. Click the *Issues* tab to 
review open issues and create new issues, if necessary.

If you need additional guidance, feel free to ask questions following the 
[support][support] guidelines.

## Bug reports

Bug reports are essential to maintain the stability and quality of this project. 
Complete bug reports will allow maintainers to reproduce the bug and gain 
insight into fixing. Since this project contains a series of notebooks rather 
than an installed package, bug reports may or may not come in the form of a 
[minimal reproducible example][reprex].

Trying out the bug-producing code on the main branch is often a worthwhile 
exercise to confirm that the bug still exists. It is also worth searching open 
issues and pull requests labeled *bug* to see if the issue has already been 
reported and/or fixed.

Bug reports must:
1. Use a clear and descriptive title for the issue to identify the problem.
2. Include a short description of the problem and supporting documentation, e.g. 
   a code snippet using [GitHub Flavored Markdown][ghmarkdown], a screenshot, or 
   a link to a screen capture.
3. Include an explanation why the current behavior is wrong/undesired and what 
   you expect instead.
5. Include the full version string of the operating system and python install.

## Feature requests

Code quality enhancements, documentation improvements, and new scientific 
analyses may be suggested by creating a new issue.

Feature requests must:
1. Use a clear and descriptive title for the issue to clarify the request.
2. Include a short description of the requested contribution and any 
   supporting documentation, e.g. a code snippet using [GitHub Flavored 
   Markdown][ghmarkdown], an image, or a link to a video.
3. Include an explanation of how the feature suggested might improve the 
   project.

## Working with the codebase

Now that you have an issue you want to fix or feature to contribute, you may 
need to learn how to work with GitHub and the `reflective-potential` codebase.

### Version control, Git, and GitHub

To the novice, working with Git is one of the more difficult aspects of 
contributing to collaborative software projects. It is easy to get 
overwhelmed, but following to the guidelines below will help keep the process 
straightforward and relatively smooth sailing. As always, if you are having 
difficulties please feel free to ask for help following the [support][support] 
guidelines.

The codebase is hosted on [GitHub][repo]. To contribute you will need to sign 
up for a [free GitHub account][signup]. [Git][git] is a version control system 
that allows many people to work together on a software project. The internet 
has an abundance of resources for learning Git and GitHub:

* [Git Guides][gitguides]
* [Git and GitHub learning resources][gitresources]
* [GitHub Learning Lab][githublearninglab]
* [Coursera Intro to Git/GitHub][gitcoursera]

### Getting started with Git

GitHub has [setup instructions][gitsetup] for installing git, setting up your
SSH key, and configuring git. All these steps need to be completed before you 
can work seamlessly between your local repository and GitHub.

### Forking

*If you are not a member of the Reflective Earth organization on GitHub, you 
need your own fork to work on the code.* Go to the project page and hit the 
Fork button in the upper right. Clone your fork to your machine:

```
git clone https://github.com/{your-user-name}/reflective-potential.git
cd reflective-potential
git remote add upstream https://github.com/reflectiveearth/reflective-potential.git
```

This creates the directory `reflective-potential` and connects your repository 
to the upstream (main project) repository.

### Development environment

*This project provides conda environment specifications for each of its 
notebooks.* These can be used with [conda][miniconda] or its optimized drop-in 
replacement, [mamba][mamba].

1. Create and activate the `conda`/`mamba` environment corresponding to the 
   notebook you would like to run.
   * e.g. environment for `01-ingest.ipynb`
     * `{conda | mamba} create --file {linux | macos}.ingest.environment.yml`
     * `conda activate ingest`
2. Launch Jupyter Lab.
   * `jupyter lab`
3. Open the Jupyter notebook you would like to run.

> *N.B.* additional setup may be required. See the *Preliminaries* section 
> of each notebook.

### Creating a branch

*This project uses the [GitHub Flow branching strategy][githubflow].* The main 
branch should reflect only production-ready code, so create a bugfix or feature 
branch before making your changes. Strive to use the `feature` prefix for 
features and the `bugfix` prefix for bugfixes, plus a short hyphenated 
description. For example:

```
git checkout -b feature/short-description
```

This changes your working directory to the feature/short-description branch. 
Keep any changes in this branch specific to one bug or feature so it is clear 
what the branch brings to the project. You can have many branches with features
and bugfixes and switch between them using the `git checkout` command.

To update your main branch, you need to retrieve the changes from the upstream 
main branch:

```
git fetch upstream
git merge upstream/main
```

This will combine your commits with the latest `reflective-potential` git main 
branch. If this leads to merge conflicts, you must resolve these before 
submitting your pull request. If you have uncommitted changes, you will need 
to git stash them prior to updating. This will effectively store your changes, 
which can be reapplied after updating.

### Contributing your changes

#### Committing your changes

Once you’ve made changes, you can see them by typing:

```
git status
```

If you have created a new file, it is not being tracked by git. Add it by 
typing:

```
git add path/to/file-to-be-added.py
```

Entering ‘git status’ again should return something like:

```
# On branch feature/short-description
#
#       modified:   /relative/path/to/file-you-added.py
#
```

Practice writing strong commit messages. Chris Beams has written some 
great [commit message guidelines][gitcommit].

First, commit your changes in your local repository:

```
git commit -m
```

### Documenting your changes

Changes should be reflected in the release notes located in 
[CHANGELOG.md][changelog]. This file contains an ongoing changelog for each 
release. Add an entry to this file to document your bugfix, enhancement, or 
scientific analysis. Make sure to put the changes sections corresponding to 
the action you took (e.g. Added, Changed, Removed) and to include the GitHub
issue number or pull request number when adding your entry (using `GH-1234`
or `PR-5678`, where `GH` refers to issues, `PR` refers to pull requests, and
the trailing number refers back to the issue or pull request number).

#### Pushing your changes

When you want your changes to appear publicly on your GitHub page, push your
forked branch commits:

```
git push origin feature/short-description
```

Origin is the default name given to your remote repository on GitHub. You can
see the remote repositories with the following command:

```
git remote -v
```

If you added the upstream repository as described above you will see something
like the following:

```
origin  git@github.com:{your-user-name}/reflective-potential.git (fetch)
origin  git@github.com:{your-user-name}/reflective-potential.git (push)
upstream  git://github.com/reflectiveearth/reflective-potential.git (fetch)
upstream  git://github.com/reflectiveearth/reflective-potential.git (push)
```

Now you have pushed your code to your fork of reflective-potential on GitHub, 
but it is not yet a part of the main reflective-potential project. For that to 
happen, a pull request needs to be submitted on GitHub.

### Make a pull request

When you are ready to request a code review, create a pull request. A pull 
request is how code from a local repository becomes available to the GitHub
community and can be reviewed and eventually merged into the main version. 
This pull request and its associated changes will eventually be committed to 
the main branch and available in the next release. To submit a pull request:

1. Navigate to your forked reflective-potential repository on GitHub
2. Click on the *Pull Request* button
3. Click on the *Commits* and *Files Changed* tabs to make sure everything looks 
   okay
5. Write a description of your changes in the *Preview Discussion* tab
6. Click *Send Pull Request*.

This request then goes to the repository maintainers, and they will review 
the code. If you need to make more changes, you can make them in your branch, 
add them to a new commit, push them to GitHub, and the pull request will 
automatically be updated. Pushing them to GitHub is accomplished by:

```
git push origin feature/short-description
```

This will automatically update your pull request with the latest code.

### Delete your merged branch (optional)

Once your feature or bugfix branch is accepted upstream, you will likely 
want to delete the branch. First, update your main branch to ensure that 
the merge was successful:

```
git fetch upstream
git checkout main
git merge upstream/main
```

Then you can delete your local branch:

```
git branch -D feature/short-description
```

The upper-case D option is necessary because the branch was squashed into
a single commit before merging. Use this command with option because git 
will let you delete an unmerged branch without warning.

If you didn’t delete your branch using GitHub’s interface, then it will 
still exist on GitHub. To delete it there, use the following command:

```
git push origin --delete feature/short-description
```

<!-- Definitions -->

[changelog]: CHANGELOG.md
[conduct]: CODE_OF_CONDUCT.md
[ghmarkdown]: https://docs.github.com/en/github/writing-on-github
[git]: http://git-scm.com/
[gitcommit]: https://chris.beams.io/posts/git-commit/
[gitguides]: https://github.com/git-guides/
[gitcoursera]: https://www.coursera.org/learn/introduction-git-github
[githubflow]: https://guides.github.com/introduction/flow/
[githublearninglab]: https://lab.github.com/
[gitresources]: https://docs.github.com/en/get-started/quickstart/git-and-github-learning-resources
[gitsetup]: https://docs.github.com/en/get-started/quickstart/set-up-git
[issue]: https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues
[mamba]: https://mamba.readthedocs.io/en/latest/
[miniconda]: https://docs.conda.io/en/latest/miniconda.html
[repo]: https://github.com/ReflectiveEarth/reflective-potential
[reprex]: https://stackoverflow.com/help/minimal-reproducible-example
[signup]: https://github.com/signup/free
[support]: SUPPORT.md
