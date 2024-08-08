import globals


class Activity:

    def __init__(self):
        pass

    def show_activity(self):
        for transaction_id, details in globals.TRANSACTIONS.items():
            print(f"Transaction ID: {transaction_id}")
            print(f"  Title      : {details['title']}")
            print(f"  Amount     : {details['amount']}")
            print(f"  Paid by    : {details['paid_name']} (User ID: {details['paid_by']})")
            print("  Contributors:")
            for contributor_id, contributor_details in details['contributors'].items():
                print(f"    - {contributor_details['name']} (User ID: {contributor_id})")
            print("-" * 40)
