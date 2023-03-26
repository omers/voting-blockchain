# Python program to create Blockchain

# For timestamp
import datetime
import time
# Calculating the hash
# in order to add digital
# fingerprints to the blocks
import hashlib

# To store data
# in our blockchain
import json

# Flask is for creating the web
# app and jsonify is for
# displaying the blockchain
from flask import Flask, jsonify, Response
from prometheus_client import Counter, generate_latest, Summary
CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')


class Blockchain:

	# This function is created
	# to create the very first
	# block and set its hash to "0"
	def __init__(self):
		self.chain = []
		self.create_block(proof=1, previous_hash='0')

	# This function is created
	# to add further blocks
	# into the chain
	def create_block(self, proof, previous_hash):
		block = {'index': len(self.chain) + 1,
				'timestamp': str(datetime.datetime.now()),
				'proof': proof,
				'previous_hash': previous_hash}
		self.chain.append(block)
		return block

	# This function is created
	# to display the previous block
	def print_previous_block(self):
		return self.chain[-1]

	# This is the function for proof of work
	# and used to successfully mine the block
	def proof_of_work(self, previous_proof):
		new_proof = 1
		check_proof = False

		while check_proof is False:
			hash_operation = hashlib.sha256(
				str(new_proof**2 - previous_proof**2).encode()).hexdigest()
			if hash_operation[:5] == '00000':
				check_proof = True
			else:
				new_proof += 1

		return new_proof

	def hash(self, block):
		encoded_block = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(encoded_block).hexdigest()

	def chain_valid(self, chain):
		previous_block = chain[0]
		block_index = 1

		while block_index < len(chain):
			block = chain[block_index]
			if block['previous_hash'] != self.hash(previous_block):
				return False

			previous_proof = previous_block['proof']
			proof = block['proof']
			hash_operation = hashlib.sha256(
				str(proof**2 - previous_proof**2).encode()).hexdigest()

			if hash_operation[:5] != '00000':
				return False
			previous_block = block
			block_index += 1

		return True


# Creating the Web
# App using flask
app = Flask(__name__)

# Setup App exposed metrics

# Create the object
# of the class blockchain
blockchain = Blockchain()

index_counter = Counter('index', 'Index Page Counter')
@app.route('/', methods=['GET'])
def index():
	index_counter.inc()
	return jsonify({"status": "OK"}), 200

@app.route('/metrics')
def metrics():
	return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# Mining a new block
mine_block_counter = Counter('mine_block', 'Mine Block Counter')
mine_duration = Summary('mine_block_duration_compute_seconds', 'Time spent in the mine_block() function')
@app.route('/mine_block', methods=['GET'])
@mine_duration.time()
def mine_block():
	st = time.time()
	mine_block_counter.inc()
	previous_block = blockchain.print_previous_block()
	previous_proof = previous_block['proof']
	proof = blockchain.proof_of_work(previous_proof)
	previous_hash = blockchain.hash(previous_block)
	block = blockchain.create_block(proof, previous_hash)
	et = time.time()
	elapsed_time = et - st
	response = {'message': 'A block is MINED',
				'index': block['index'],
				'elapsed': elapsed_time,
				'timestamp': block['timestamp'],
				'proof': block['proof'],
				'previous_hash': block['previous_hash']}

	return jsonify(response), 200

# Display blockchain in json format

get_chain_counter = Counter('get_chain', 'Get Chain URL Counter')
@app.route('/get_chain', methods=['GET'])
def get_chain():
	get_chain_counter.inc()
	response = {'chain': blockchain.chain,
				'length': len(blockchain.chain)}
	return jsonify(response), 200

# Check validity of blockchain

valid_block_counter = Counter('valid', 'Mine Block Counter')
valid_duration = Summary('valid_duration_compute_seconds', 'Time spent in the valid() function')
@app.route('/valid', methods=['GET'])
@valid_duration.time()
def valid():
	valid_block_counter.inc()
	valid = blockchain.chain_valid(blockchain.chain)

	if valid:
		response = {'message': 'The Blockchain is valid.'}
	else:
		response = {'message': 'The Blockchain is not valid.'}
	return jsonify(response), 200


# Run the flask server locally
app.run(host='0.0.0.0', port=5001)

