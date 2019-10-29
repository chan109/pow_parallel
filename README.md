This script is to solve proof of work problem. It use arbitary nonce to compute hash. 
The goal is to find the nonce such that its hash ends with sufficient number of zero.

In order to make the finding faster, python multiprocessing is introduced in the script for using more cpu power finding the answer.
