# Contributing to Livecli

Want to get involved? Thanks! There are plenty of ways to help!


## Reporting issues

A bug is a *demonstrable problem* that is caused by the **latest version** of the code in the repository.

Please read the following guidelines before you [report an issue][issues]:

1. **See if the issue is already known** — check the list of [known issues][known-issues].

2. **Use the GitHub issue search** — check if the issue has already been reported. If it has been, please comment on the existing issue.

3. **Check if the issue has been fixed** — the latest `master` or development branch may already contain a fix.

4. **Isolate the demonstrable problem** — make sure that the code in the project's repository is *definitely* responsible for the issue.

## Feature requests

Feature requests are welcome, but take a moment to find out whether your idea fits with the scope and aims of the project.


## Plugin requests

Plugin submissions and requests are a great way to improve Livecli. Requests should be as detailed as possible and dedicated to only a single streaming service.

Please be aware that plugins for streaming services that are using DRM protections or
websites from not official or not authored third party **will not be implemented**.

## Pull requests

Good pull requests - patches, improvements, and new features - are a fantastic help. They should remain focused in scope and avoid containing unrelated commits.

**Please ask first** before embarking on any significant pull request (e.g. implementing features, refactoring code, porting to a different language), otherwise you risk spending a lot of time working on something that the project's developers might not want to merge into the project.

Please adhere to the coding conventions used throughout a project (indentation, white space, accurate comments, etc.) and any other requirements (such as test coverage).

Adhering to the following process is the best way to get your work included in the project:

1. [Fork][howto-fork] the project, clone your fork, and configure the remotes:
   ```bash
   # Clone your fork of the repo into the current directory
   git clone git@github.com:<YOUR-USERNAME>/livecli.git
   # Navigate to the newly cloned directory
   cd livecli
   # Assign the original repo to a remote called "upstream"
   git remote add upstream https://github.com/livecli/livecli.git
   ```

2. If you cloned a while ago, get the latest changes from upstream
   ```bash
   git checkout master
   git pull upstream master
   ```

3. Create a new topic branch (off the main project branch) to contain your feature, change, or fix:
   ```bash
   git checkout -b <TOPIC-BRANCH-NAME>
   ```

4. Commit your changes in logical chunks. Please adhere to these [git commit message guidelines][howto-format-commits] or your code is unlikely be merged into the project. Use git's [interactive rebase][howto-rebase] feature to tidy up your commits before making them public.

5. Locally merge (or rebase) the upstream branch into your topic branch:
   ```bash
   git pull [--rebase] upstream master
   ```

6. Push your topic branch up to your fork:
   ```bash
   git push origin <TOPIC-BRANCH-NAME>
   ```

7. [Open a Pull Request][howto-open-pull-requests] with a clear title and description.

**IMPORTANT**: By submitting a patch, you agree to allow the project owners to license your work
under the terms of the [BSD 2-clause license][license].


## Acknowledgements

This contributing guide has been adapted from [HTML5 boilerplate's guide][ref-h5bp].


  [issues]: https://github.com/livecli/livecli/issues
  [known-issues]: https://github.com/livecli/livecli/blob/master/KNOWN_ISSUES.md
  [issue-template]: https://github.com/livecli/livecli/blob/master/ISSUE_TEMPLATE.md
  [mastering-markdown]: https://guides.github.com/features/mastering-markdown
  [howto-fork]: https://help.github.com/articles/fork-a-repo
  [howto-rebase]: https://help.github.com/articles/interactive-rebase
  [howto-format-commits]: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
  [howto-open-pull-requests]: https://help.github.com/articles/using-pull-requests
  [Git]: https://git-scm.com
  [license]: https://github.com/livecli/livecli/blob/master/LICENSE
  [ref-h5bp]: https://github.com/h5bp/html5-boilerplate/blob/master/CONTRIBUTING.md
