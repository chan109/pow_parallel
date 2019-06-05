import hashlib
import multiprocessing
import logging
import argparse
import time
import datetime

"""
    The object to problem is to find the secret such that the computed hash of nonce + secret contain sufficicent number of "0" at the end.
    
    This problem makes use of multiprocessing and pipe to solve pow.
    
    
"""

def add_score(name, user_profile):
  for user in user_profile:
      if user == name:
         user_profile[user] += 1

def print_winner(user_profiles):
    winner = []
    winner_score = -1
    for name in user_profiles:

        user_score = users_profiles[name]
        if user_score > winner_score:
            winner_score = user_score
            winner = [name]
        elif user_score == winner_score:
            winner.append(name)


    print("The winner is %s" % winner)

def proof_of_work_fast(nonce, first_guess, difficulity, conn):

    guess = first_guess

    while True:
        computed_hash = hashlib.sha256((str(nonce) + str(guess)).encode('utf-8')).hexdigest()
        if check_hash(computed_hash, difficulity):
            conn.send([computed_hash, guess, multiprocessing.current_process().name])
            return computed_hash, guess

        guess = computed_hash

    print(
        "Elapsed time: %.4f seconds" % elapsed_time
    )

def check_hash(hash, difficulity):
    """
    Check if the computed has enough zeroes at the end
    """
    for i in range(len(hash)-1, len(hash)-1-difficulity, -1):
        if hash[i] != '0':
            return False
    return True

def parallel_run(problem, difficulity, users_profiles):

    rec_channel, send_channel = multiprocessing.Pipe()
    problem = 'Nonce to compute ' + str(problem)
    procs = []

    # (Init processes) Create number of processes for parallel computing
    for uname in users_profiles:
      procs.append(multiprocessing.Process(target=proof_of_work_fast, name=uname, args = (problem, uname, difficulity, send_channel)))

    #(Start all process) Start processes
    for p in procs:
      p.daemon=True
      p.start()

    # (blocking call) Wait till one of the children processes sends the result.
    result = rec_channel.recv()

    # Add the score to the winner
    add_score(result[2], users_profiles)

    for p in procs:
      p.terminate()

    for p in procs:
      p.join()

    print("\n[%s] found secret, [%s]\nThe computed hash is %s.\n" % (result[2], result[1], result[0]))

if __name__ == '__main__':

    # Get difficulity from user
    parser = argparse.ArgumentParser(description="Enter the difficulity for the pow.")
    parser.add_argument('difficulity', metavar="Difficulity", type=int, help="An integer for the difficulity of the pow.")
    args = parser.parse_args()
    difficulity = args.difficulity

    # Setup for logging
    # multiprocessing.log_to_stderr()
    # logger = multiprocessing.get_logger()
    # logger.setLevel(logging.INFO)

    print("\n")
    print('Starting parallel mode: \n')

    # Init the users_profiles
    first_guesses = ["michael", "Stevent", "Chris", "Ruslan", "Max", "Yulian", "Garisson", "Anindya"]
    users_profiles = {}
    for i in range(len(first_guesses)):
        users_profiles[first_guesses[i]] = 0

    for i in range(5):
        # The problem to solve is the current timestamp
        print("----------------------------------Trial #%s\n" % i)
        start_time = time.time()
        problem = datetime.datetime.now().isoformat()
        print("The problem string is %s\n" % problem)

        parallel_run(problem, difficulity, users_profiles)
        print("The current user profile: %s\n" % str(users_profiles))
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(
            "Elapsed time: %.4f seconds\n" % elapsed_time
        )

    print_winner(users_profiles)

