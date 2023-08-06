# rand_api

`rand_api` is a Python module that provides a simple API for generating random data.

## Installation

You can install `rand_api` using pip:


## Usage

Here's an example of how to use `rand_api` to generate a random integer between 0 and 10:


import rand_api

rand_int = rand_api.rand_int(0, 10)
print(rand_int)

API documentation
rand_api.rand_int(min: int, max: int) -> int
Generate a random integer between min and max, inclusive.

rand_api.rand_float(min: float, max: float) -> float
Generate a random float between min and max.

rand_api.rand_bool() -> bool
Generate a random boolean value.

rand_api.rand_bytes(length: int) -> bytes
Generate a random byte string of length length.

rand_api.rand_string(length: int, charset: str) -> str
Generate a random string of length length, using characters from the charset string.

rand_api.rand_choice(seq: Sequence[T]) -> T
Return a random element from the given sequence seq.

License
rand_api is released under the MIT License.

Contact
If you have any questions or issues with rand_api, please contact us at chrisfdas1@gmail.com.