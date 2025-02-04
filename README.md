# rustmaps_generator
Attempts to generate as many Rust Maps as possible for given size as your rustmaps.com API limits allow it to

## Usage
python3 map_gen.py

## Config
There are two variables you HAVE TO adapt before starting:
- api_key (Your API key from rustmaps.com)
- size (The map size you want to generate)

And a few more you SHOULD adapt to your needs:
- staging (whether or not the generated maps should be for the staging branch)
- seed_history (the file that stores the seeds previously used for generation to avoid duplicates)
- retry_interval (The amount of seconds to wait between generation attempts)

## Further information
Currently, the output is the raw JSON response, which will be changed in later commits.
