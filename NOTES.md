# requirements.txt changes
Updated requirements.txt as was used locally.
The specified versions of pytest and flask were outdated and had bugs.
I am assuming this is due to requirements not recently updated and not intended,
that is why i chose to update them.

# bitly requires token
bitly requires token corresponding to a user account.
In this implementation, the necessary variables
BITLY_TOKEN and GROUPGUID are saved as enviroment variables and drawn from there.
using virtualenvwrapper package an environment was created where 
post activate script declared the necessary environment variables.

# response codes
502 -> Both third party apis return response code greater than 499.
500 -> At least one third party api returned error code between 400-499. Or an unhandled exception was raised.
400 -> User input is malformed.
200 -> Everything worked as expected!

# basic structure
The two third party apis are queried using the functions shorturl.tinyURL and shorturl.bitly.
In order to replace these apis or add new ones one should simply add a new function for the new api, 
and adjust shorturl.providersInterface (define priorities for more than 2 providers) and helper.getQueryParameters
to allow the new provider name as input.
