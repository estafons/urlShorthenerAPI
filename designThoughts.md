# create two different functions corresponding to each third party api
This way, if changes need to be made to one of the two, this can be handled by changing associated
function and it is easier to maintain and change as well as use it on other cases. 

# created specific function for env vars
In order to be easily testable and adaptable to other cases too.

# for bitly, create a group with user permissions
create group with user (non-elevated) permissions to improve security. Token will be associated and called with this group guid.

# on tests, check for random characters how api behaves
check if url posted is same as returned.

# flask version bug for 1.0.2 and pytest updated

# distringuish backend functionality from view
