1. Users can enter the lottery with ETH based on a USD fee.
2. An admin will choose when the lottery is over.
3. The lottery will select a random winner.

How do we want to test this?

1. `mainnet-fork`
2. `development` with mocks
3. `testnet`

IMPORTANT: Need help with an error, on running the final 'brownie run scripts/deploy.py --network rinkeby' command, which deploys it on the actual test-net.

Error: ValueError: Gas estimation failed: 'execution reverted'. This transaction will likely revert. If you wish to broadcast, you must set the gas limit manually.
