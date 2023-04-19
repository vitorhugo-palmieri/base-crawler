# CONTRIBUTING

## How to develop a crawler

In order to develop a crawler, some steps should be followed.

1. Create a crawler using the crawler-template project. For more information, check crawler-template README.
2. Write id_fields and required_keys in your spider.py class to avoid a CreateSpiderException.
3. Create a function in parser.py to validate input
4. Create a test for this function in parser_tests.py. Run your tests to make sure that the function is working properly.
5. Create your first request in spider.py and debug its response using the self.debug_response function. Check BaseSpider class for more information.
6. Run the integration tests for the request to actually happen.
7. The response file will be saved in the tests/files/debug folder. Create a tests/files/tests_files folder and move it to this folder. The folder **must** have this name.
8. Create a function in the parser to validate the response, create a test for this function, run the unit tests.

   8.1. Use the functions in the test_helper to read the file from the tests folder. For JSON files, there's no need to put the extension in the file name, just use the appropriate functions to deal with json files.
   8.2. The test_helper is located in this project -> tests/test_helper.py

9. Repeat, and keep programming the flow on your spider, the funcions in your parser and unit tests for these functions.

10. Rememeber to update the CHANGELOG file in your crawler to include the newest changes.


## How to deploy a crawler

The steps to deploy a crawler are described below:

1. Create a branch named config/ci-cd from main if the bot is merged or from the branch that is currently in MR.
2. Add the file .gitlab-ci.yml and update the `CI_REGISTRY` variable to the following: `CI_REGISTRY: registry.gitlab.com/b252/{your-crawler-name}`
3. Change the Dockerfile FROM to registry.gitlab.com/b252/base-crawler and --from in the COPY instruction.
4. Create a merge request to the branch config/ci-cd.
5. If everything is ok by a reviewer, apply the merge to the branch.
6. Wait for the pipeline to run. If the pipeline passes, talk to dev ops team to deploy the bot. Keep in mind all the environment variables needed. They're usually in the docker-compose file of the bot.

### Attention

If there's an update in base-crawler, it must be merged to the config/ci-cd branch. Create a merge request first, to be validated by someone else.

After the pipeline runs after the merge is applied, you must go to the CI/CD -> Pipelines page in Gitlab of each bot.

Then, click the button "Run pipeline", choose the config/ci-cd branch and let the pipeline run again. This will make the bot download the new base crawler image and generate a new image.

Finally, the dev ops team should be contacted to deploy this bot.

### Next steps - Deploy

There will be the need to create different git tags for each deployed version. It's important to keep the CHANGELOG file updated.

Then, a new git tag should be generated for each version. Then, this tag will be the version used by the new image in production after the pipeline is run. Today, it is "latest" but this will be versioned using SemVer. For more information about versioning, take a look at the CHANGELOG file.