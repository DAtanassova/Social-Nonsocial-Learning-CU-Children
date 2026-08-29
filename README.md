SPARK Zoo is a probabilistic reversal-learning task designed for children aged 4 years and above. The task takes approximately 8 minutes to complete and is designed to run in Python using PsychoPy 2022 for best compatibility.

**Paradigm Description**
On each trial, children see an animal enclosure with an animal in the centre (fixation) for 600±150 ms. Two food options then appear on either side of the animal. Children have 5 seconds to choose which food to offer to the animal. The food options are selected to be appropriate for the animal (e.g., fish and apples for a bear). Children choose the left food option by pressing A or the right food option by pressing C. If no response is made within 5 seconds, the screen displays “Too slow!” accompanied by a sound. If a response is made, an outcome is presented for 950 ms. After the outcome, an empty animal enclosure is presented for 700 ± 150 ms, after which the next trial begins.

**Social condition**
In the social condition, the outcome is presented as the face of a junior zookeeper (another child) on a display board. Correct choices result in a smiling expression, whereas incorrect choices result in a frowning expression. The perceptual ambiguity of the facial expression is experimentally manipulated using the variable Perc_Unc, with higher values indicating greater ambiguity.

**Non-social condition**
In the non-social condition, the same display board is presented with a symbolic outcome instead of a face: a check mark indicates a correct choice and an X mark indicates an incorrect choice. The perceptual ambiguity of these symbols is also experimentally manipulated.

**Task Structure**
The task comprises 80 trials, with 40 trials per condition (40 social and 40 non-social). Two animals are currently used, one for each condition: rhino and bear.
The task consists of an initial stable acquisition block, followed by multiple reversal blocks. During reversals, the food option associated with the higher probability of reward changes, requiring children to update their expectations and adapt their choices.
The order of the social and non-social conditions is pseudo-randomised based on participant number. 
- Even participant numbers: social condition first. 
- Odd participant numbers: non-social condition first

**Practice**
When practice mode is enabled in the pop-up menu, the task begins with a short 7-trial practice run, during which social and non-social outcomes are mixed. A different face stimulus is used during practice to avoid exposing children to one of the experimental face stimuli before the main task.

**Instructions**
Given the young age of the participants, instructions are not presented within the task. Instead, we recommend providing instructions before the task begins by showing the child the different possible outcomes and familiarising them with the buttons they will use to respond.

**Image Attribution**
The faces used in the task are retrieved from the Radboud Faces Database (RaFD): https://rafd.nl/.
Other images were Designed by Magnific and are used with the required attribution: www.magnific.com.

**Compatability with EEG**
The task is designed to be used with EEG: the EEG component can be enabled in the pop-up menu, in which
case the task runs as a simple behavioural paradigm. 

**How to start the task**
Download the entire folder "Social-Nonsocial-Learning-Zoo-Task". To run the task, open the "SPARK_Zoo_Task.py" in PsychoPy (or another Python shell). 
When you start the task, you will be prompted to enter a participant number, as well as select the session settings.
Indicate if the session is a practice (in which case, a shorter sequence will be run), and whether there is an EEG system connected.
When prompted, press SPACE to begin the task. You can pause the task at any moment by pressing **SPACE**. 
To quit the task at any moment, press **Escape**.

