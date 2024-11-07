## Description
**Please provide a brief description of the changes made in this pull request.**

## Issue linked
**Please mention the issue number or describe the problem this pull request addresses.**

## Checklist:
- [] Run unit tests and make sure they all pass
		- Run tests without Sherlock running
		- Run tests with Sherlock GRPC connection
- [] Check and fix style errors
		- pre-commit command line check
		- Problems tab in PyCharm
- [] Bench test new/modified APIs by using and modifying the code in the example for the API method
- [] Add new classes to rst files, located at: <pysherlock>\doc\source\api
- [] Generate documentation
- [] Verify the HTML. It gets generated at: <pysherlock>\doc\build\html.
		- Open index.html
		- Click on "API Reference" at the top.
		- Verify HTML for API changes.
- [] Check that test code coverage is at least 80% when Sherlock is running
- [] Make sure the the title of the pull request follows [Commit naming conventions](https://dev.docs.pyansys.com/how-to/contributing.html#commit-naming-conventions) (e.g. ``feat: adding new PySherlock command``)
