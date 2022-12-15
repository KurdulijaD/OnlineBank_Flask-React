from Configuration.config import api, jsonify, db, activeTokens, make_response
from flask_restful import Resource
from Models.__init__ import Transaction, TransactionSchema
from Configuration.config import reqparse
from Processing.__init__ import addTransaction

transactionArgs = reqparse.RequestParser()
transactionArgs.add_argument("type", type=int, help="Type of transaction is required", required = True)
transactionArgs.add_argument("receiver", type=str, help="Receiver (User email or account number) is required", required = True)
transactionArgs.add_argument("amount", type=float, help="Amount can't be 0 and it's required", required = True)
transactionArgs.add_argument("currency", type=str, help="Currency is required", required = True)

#Transaction get (history) and post (making new transaction)
class TransactionProfile(Resource):
    def get(self, token):
        """ Get all transaction for a given user (token) """
        try:
            if token not in activeTokens.keys():
                return "Please login to continue.", 404
            email = activeTokens[token]

            transactionSender = db.session.execute(db.select(Transaction).filter_by(sender=email)).all()
            transactionReceiver = db.session.execute(db.select(Transaction).filter_by(receiver=email)).all()
            
            transaction = transactionSender + transactionReceiver
            if len(transaction) == 0:
                return "There is no transaction", 200
            result = TransactionSchema(many=True).dumps(transaction)
            return make_response(jsonify(result), 200)            
        except Exception as e:
            return 'Error: ' + str(e), 500
            
    def post(self, token):
        args = transactionArgs.parse_args()

        try:
            if token not in activeTokens.keys():
                return "Please login to continue.", 404
            email = activeTokens[token]

            addTransaction(token, (email, args['receiver'], args['amount'], args['currency'], args['type']))
        except Exception as e:
            return 'Error: ' + str(e), 500
api.add_resource(TransactionProfile, "/transaction/<string:token>")

