# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/), and this project adheres to [Semantic Versioning](https://semver.org)

## [1.0.0]
 - Extract create item id function to helper module (@Paulo-oRicardo)
 - Filter already downloaded decisions tjsp (@Paulo-oRicardo)
 - Adding judgment court normalizer (@pedrobarbosadev) 
 - Make_treatment_of_ementa (@Paulo-oRicardo)
 - Adding missing fields to common-schema (@vavieira10)
 - Adding captchav3 solver (@vavieira10)
 - Adding anticaptcha provider (@vavieira10)
 - Adding transformed_outputs database for saving treated data from the pipeline (@vavieira10)
 - Adding sistema field to common-schema (@vavieira10)
 - Improving unit test scripts for being generic (@vavieira10) 
 - Adding normalizer for area field (@vavieira10)
 - Creating unit test files for each normalizer. Created rapporteur_normalizer tests (@vavieira10)
 - Add documentation (@Silver472)
 - Add bucket module to communicate with OCI bucket (@Silver472)
 - Concurrency count as environment variable (@Silver472)
 - All strings in "data" key are transformed to upper case and stripped (@Silver472)
 - Add rapporteur normalization (@Silver472)
 - Implement schema final version (@Silver472)
 - Add support for captcha V2 and image solving (@Silver472)
 - Add common schema to all bots (@Silver472)
 - Add pipeline to communicate with elasticsearch (@Silver472)
 - Add function in helper to find element in array by a lookup
 - Change debug_response_file method in BaseSpider to save a file with the same name by creating an automatic sequence number to the file name (@Silver472)
 - Change function interfaces for test_helper (@Silver472)
 - Add datetime conversion to UTC in helper (@Silver472)
 - Add metadata to schema with processingDate and spiderName (@Silver472)
 - Add RabbitMQ input feature (@Silver472)
 - Create BaseSpider, pipeline unit tests, spider tests and fixtures, base exceptions and helper (@Silver472)
  