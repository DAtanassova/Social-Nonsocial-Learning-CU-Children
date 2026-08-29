#!/usr/bin/env python3

import os
import sys
import csv
import random
from datetime import datetime

from psychopy import core, visual, event, sound, gui, prefs
from psychopy.hardware import keyboard

# =============================================================================
# PsychoPy audio settings
# =============================================================================

prefs.hardware['audiolib'] = ['ptb']

# =============================================================================
# Paths
# =============================================================================

script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'stimuli')

# =============================================================================
# Dynamic image sizing
# =============================================================================

def get_fullscreen_image_size(win):
    return win.size
    
# =============================================================================
# Session / schedule
# =============================================================================

def getSession(isPractice, participant):

    if isPractice:
        print("Currently running the Practice Run.")
        filename = os.path.join(
            script_dir,
            'schedule_practice.csv'
        )
        task_version = "Practice"

    else:
        if int(participant) % 2 != 0:
            filename = os.path.join(
                script_dir,
                'schedule_nonsocial_first.csv'
            )
            task_version = "A"
            print("Task version A: odd participant, nonsocial first")

        else:
            filename = os.path.join(
                script_dir,
                'schedule_social_first.csv'
            )
            task_version = "B"
            print("Task version B: even participant, social first")

    with open(filename, 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        trials = list(reader)

    return trials, task_version


# =============================================================================
# EEG marker
# =============================================================================

def sendMarker(isEEG, cc, markerNumber):

    if isEEG:
        cc.sendMarker(val=markerNumber)
        core.wait(0.002)
        cc.sendMarker(val=0)

    else:
        print('[EEG MOCK] sent marker {}'.format(markerNumber))


# =============================================================================
# Image lookup
# =============================================================================

def lookup_image(animal, stim1, stim2):

    filename = f"{animal}_{stim1}_{stim2}.png"
    filepath = os.path.join(image_path, filename)

    if os.path.exists(filepath):
        return filepath

    else:
        print('IMAGE ERROR:', filepath)
        return None


# =============================================================================
# Run task
# =============================================================================

def runtrials(
    win,
    writer,
    datafile,
    expData,
    Task,
    participant,
    isPractice,
    isEEG,
    cc
):

    # -------------------------------------------------------------------------
    # Load schedule
    # -------------------------------------------------------------------------

    trials, task_version = getSession(
        isPractice,
        participant
    )

    expData['Participant'] = participant
    expData['Practice'] = isPractice
    expData['EEG'] = isEEG
    expData['TaskVersion'] = task_version

    # -------------------------------------------------------------------------
    # Column indices in schedule CSV
    # -------------------------------------------------------------------------

    BlockNumberIndex = 0
    TrialNumberIndex = 1
    Animal = 2
    Stim1_name = 3
    Stim2_name = 4
    Stim1_outcome = 5
    Stim2_outcome = 6
    ProbStim1 = 7
    PercUnc_label = 8
    Condition = 9
    Identity = 10
    TrialType = 11

    # -------------------------------------------------------------------------
    # Visual stimuli
    # -------------------------------------------------------------------------
     
    image_aspect = 4512 / 2531
    screen_aspect = win.size[0] / win.size[1]
    if screen_aspect >= image_aspect:
    # Screen is wider than the image
        fullscreen_size = (2 * image_aspect / screen_aspect, 2)
    else:
    # Screen is narrower than the image
        fullscreen_size = (2, 2 * screen_aspect / image_aspect)
    
    fixation_image = visual.ImageStim(
        win,
        pos=(0, 0),
        size=fullscreen_size,
        interpolate=True
    )

    crossroad_image = visual.ImageStim(
        win,
        pos=(0, 0),
        size=fullscreen_size,
        interpolate=True
    )

    outcome_image = visual.ImageStim(
        win,
        pos=(0, 0),
        size=fullscreen_size,
        interpolate=True
    )

    ITI_image = visual.ImageStim(
        win,
        pos=(0, 0),
        size=fullscreen_size,
        interpolate=True
    )

    ITI_image.setImage(
        os.path.join(image_path, "ITI_screen.png")
    )

    # -------------------------------------------------------------------------
    # Audio
    # -------------------------------------------------------------------------

    audioStim_foods = os.path.join(
        image_path,
        'food_appears_sound.wav'
    )

    audioStim_outcome = os.path.join(
        image_path,
        'outcome_appears.wav'
    )

    audioStim_missed_trial = os.path.join(
        image_path,
        'missed_trial_sound.wav'
    )

    # -------------------------------------------------------------------------
    # Instructions
    # -------------------------------------------------------------------------

    instructions_image = visual.ImageStim(
        win,
        pos=(0, 0),
        size=fullscreen_size,
        interpolate=True
    )

    instructions_image.setImage(
        os.path.join(
            image_path,
            "instructions_image_zoo_with_text.png"
        )
    )

    instructions_music_file = os.path.join(
        image_path,
        'instructions_music_zoo.wav'
    )

    instructions_music = sound.Sound(
        instructions_music_file,
        stereo=True,
        loops=-1
    )

    instructions_image.draw()
    instructions_music.play()
    win.flip()

    event.waitKeys(keyList=["space"])

    instructions_music.stop()

    # -------------------------------------------------------------------------
    # Experiment clock
    # -------------------------------------------------------------------------

    expClock = core.Clock()

    expData['StartExperiment'] = expClock.getTime()
    expData['StartDate'] = start_date
    expData['StartTime'] = start_time

    # =========================================================================
    # TRIAL LOOP
    # =========================================================================
    # Keep track of the current task block
    currentblock_n = 0

    for i, trial in enumerate(trials):

        # ---------------------------------------------------------------------
        # Basic trial information
        # ---------------------------------------------------------------------

        trialClock = expClock.getTime()

        expData['Block'] = trial[BlockNumberIndex]

        # ---------------------------------------------------------------------
        # Block segment
        # ---------------------------------------------------------------------

        newblock_n = int(trial[BlockNumberIndex])

        # First task block
        if currentblock_n == 0:
            currentblock_n = newblock_n

        # Between-block message when the block changes
        elif newblock_n != currentblock_n:

            condition_change_message = visual.TextStim(
                win,
                alignHoriz="center",
                text="Great job! You finished this part! \n\n"
                     "Get ready for the next part.\n\n"
                     "Press SPACE to continue.",
                pos=(0, 0.65)
            )

            condition_change_message.draw()

            condition_change_image = visual.ImageStim(
                win,
                pos=(0, -0.35),
                size=(0.9, 0.6),
                interpolate=True)

            condition_change_image.setImage(
                os.path.join(image_path, "pause_zoo.png")
            )

            condition_change_image.draw()

            instructions_music.play()
            win.flip()

            currentblock_n = newblock_n

            event.waitKeys(keyList=["space"])

            instructions_music.stop()

        expData['StartTrial'] = trialClock
        expData['Trial'] = trial[TrialNumberIndex]
        expData['Animal'] = trial[Animal]
        expData['Stim1'] = trial[Stim1_name]
        expData['Stim2'] = trial[Stim2_name]
        expData['ProbStim1'] = trial[ProbStim1]
        expData['AmbiguityLevel'] = trial[PercUnc_label]
        expData['Condition'] = trial[Condition]
        expData['OutcomeIdentity'] = trial[Identity]
        expData['TrialType'] = trial[TrialType]

        # ---------------------------------------------------------------------
        # Timing
        # ---------------------------------------------------------------------

        fixation_time = random.gauss(0.6, 0.15)
        ITI_time = random.gauss(0.7, 0.15)
        outcome_pres_time = 0.95

        # Prevent negative durations
        fixation_time = max(0.1, fixation_time)
        ITI_time = max(0.1, ITI_time)

        # ---------------------------------------------------------------------
        # Fixation
        # ---------------------------------------------------------------------

        expData['fixation_duration'] = fixation_time
        expData['fixation_start_time'] = expClock.getTime()

        fixation_image_filename = (
            f"fixation_{trial[Animal]}.png"
        )

        fixation_path = os.path.join(
            image_path,
            fixation_image_filename
        )

        fixation_image.setImage(fixation_path)
        fixation_image.draw()
        win.flip()

        sendMarker(isEEG, cc, 10)

        core.wait(fixation_time)

        # ---------------------------------------------------------------------
        # Cues
        # ---------------------------------------------------------------------

        cue_path = lookup_image(
            trial[Animal],
            trial[Stim1_name],
            trial[Stim2_name]
        )

        if cue_path is None:
            raise FileNotFoundError(
                f"Could not find cue image for "
                f"{trial[Animal]}_{trial[Stim1_name]}_{trial[Stim2_name]}"
            )

        crossroad_image.setImage(cue_path)
        crossroad_image.draw()

        sound_cues = sound.Sound(
            audioStim_foods,
            stereo=True
        )

        sound_cues.play()

        choiceStimClock = core.Clock()
        
        kb.clearEvents()
        
        choiceStimClock.reset()

        win.flip()

        expData['cues_start_time'] = expClock.getTime()
        
        sendMarker(
            isEEG,
            cc,
            20
        )

        # ---------------------------------------------------------------------
        # Choice
        # ---------------------------------------------------------------------
        
        # Clear any previous keyboard events
        kb.clearEvents()

        choice_input = event.waitKeys(
            maxWait=5,
            keyList=[
                "a",
                "l",
                "escape",
                "space"
            ],
            timeStamped = choiceStimClock,
            clearEvents=True
        )

        expData['choice_start_time'] = expClock.getTime()

#        if choice_input:
#            choice_rt = choice_input[0]
        # ---------------------------------------------------------------------
        # No response
        # ---------------------------------------------------------------------

        if not choice_input:

            expData['ButtonPress'] = 'NA'
            expData['RT'] = 'NA'

            stim_chosen = 'NA'
            stim_chosen_label = 'NA'
            outcome_event = 'NA'

            error_nothing_selected = visual.TextStim(
                win,
                pos=(0, 0),
                text='Too slow!'
            )

            error_nothing_selected.draw()

            missed_trial_cue = sound.Sound(
                audioStim_missed_trial,
                stereo=True
            )

            missed_trial_cue.play()

            win.flip()

            sendMarker(
                isEEG,
                cc,
                199
            )

            core.wait(1)

        # ---------------------------------------------------------------------
        # Response received
        # ---------------------------------------------------------------------

        else:

            choice_key = choice_input[0][0]
            choice_rt = choice_input[0][1] * 1000

            # Save response
            expData['ButtonPress'] = choice_key
            expData['RT'] = choice_rt

            # ---------------------------------------------------------------
            # Escape
            # ---------------------------------------------------------------

            if choice_key == 'escape':

                win.close()
                core.quit()

            # ---------------------------------------------------------------
            # Pause
            # ---------------------------------------------------------------

            elif choice_key == 'space':

                pause_text = visual.TextStim(
                    win,
                    pos=(0, -10),
                    text='Task paused. Press SPACE to re-start.'
                )

                pause_text.draw()
                win.flip()

                event.waitKeys(
                    keyList=["space"]
                )

                # Re-start the choice period after pause
                choiceStimClock.reset()

                choice_input = event.waitKeys(
                    maxWait=5,
                    keyList=["a", "l", "escape", "space"],
                    timeStamped = choiceStimClock,
                    clearEvents=True
                )

                if not choice_input:

                    expData['ButtonPress'] = 'NA'
                    expData['RT'] = 'NA'

                    stim_chosen = 'NA'
                    stim_chosen_label = 'NA'
                    outcome_event = 'NA'

                    sendMarker(
                        isEEG,
                        cc,
                        199
                    )

                else:

                    choice_key = choice_input[0].name
                    choice_rt = choice_input[0].rt

                    expData['ButtonPress'] = choice_key
                    expData['RT'] = choice_rt

            # ---------------------------------------------------------------
            # A = left stimulus
            # ---------------------------------------------------------------

            if choice_key == 'a':

                stim_chosen = "Stim1"
                stim_chosen_label = trial[Stim1_name]

                if trial[Stim1_outcome] == '1':

                    sendMarker(
                        isEEG,
                        cc,
                        52
                    )

                    outcome_event = "correct"

                else:

                    sendMarker(
                        isEEG,
                        cc,
                        51
                    )

                    outcome_event = "incorrect"

            # ---------------------------------------------------------------
            # C = right stimulus
            # ---------------------------------------------------------------

            elif choice_key == 'l':

                stim_chosen = "Stim2"
                stim_chosen_label = trial[Stim2_name]

                if trial[Stim2_outcome] == '1':

                    sendMarker(
                        isEEG,
                        cc,
                        54
                    )

                    outcome_event = "correct"

                else:

                    sendMarker(
                        isEEG,
                        cc,
                        53
                    )

                    outcome_event = "incorrect"

            # ---------------------------------------------------------------
            # Anything else
            # ---------------------------------------------------------------

            else:

                stim_chosen = "NA"
                stim_chosen_label = "NA"
                outcome_event = "NA"

                sendMarker(
                    isEEG,
                    cc,
                    50
                )

        # ---------------------------------------------------------------------
        # Save choice information
        # ---------------------------------------------------------------------

        expData['StimChosen'] = stim_chosen
        expData['StimChosenLabel'] = stim_chosen_label
        expData['OutcomeEvent'] = outcome_event

        # ---------------------------------------------------------------------
        # Outcome
        # ---------------------------------------------------------------------

        if outcome_event == "incorrect":

            outcome_filename = (
                f"{trial[Condition]}_"
                f"{trial[Identity]}_"
                f"negative_"
                f"{trial[PercUnc_label]}.png"
            )

            outcome_path = os.path.join(
                image_path,
                outcome_filename
            )

            outcome_image.setImage(outcome_path)

        elif outcome_event == "correct":

            outcome_filename = (
                f"{trial[Condition]}_"
                f"{trial[Identity]}_"
                f"positive_"
                f"{trial[PercUnc_label]}.png"
            )

            outcome_path = os.path.join(
                image_path,
                outcome_filename
            )

            outcome_image.setImage(outcome_path)

        else:
            outcome_path = None

        # ---------------------------------------------------------------------
        # Present outcome
        # ---------------------------------------------------------------------

        if outcome_event in ["correct", "incorrect"]:

            sound_outcome = sound.Sound(
                audioStim_outcome,
                stereo=True
            )

            sound_outcome.play()

            outcome_image.draw()
            win.flip()

            sendMarker(
                isEEG,
                cc,
                100
            )

            expData['outcome_start_time'] = expClock.getTime()
            expData['outcome_duration_time'] = outcome_pres_time

            core.wait(outcome_pres_time)

        # ---------------------------------------------------------------------
        # ITI
        # ---------------------------------------------------------------------

        ITI_image.draw()
        win.flip()

        expData['ITI_start_time'] = expClock.getTime()
        expData['ITI_duration'] = ITI_time

        core.wait(ITI_time)

        # ---------------------------------------------------------------------
        # Save trial
        # ---------------------------------------------------------------------

        writer.writerow(expData)
        datafile.flush()

    # =========================================================================
    # Goodbye
    # =========================================================================

    goodbye = visual.TextStim(
        win,
        text="Thank you for participating",
        pos=(0, 0)
    )

    goodbye.draw()
    win.flip()

    core.wait(1.0)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    # =========================================================================
    # Session setup
    # =========================================================================

    expInfo = {
        'Practice mode': False,
        'EEG connected': False,
        'Participant number': ''
    }

    dlg = gui.DlgFromDict(
        dictionary=expInfo,
        title='Experiment Settings',
        order=[
            'Participant number',
            'Practice mode',
            'EEG connected'
        ]
    )

    if not dlg.OK:
        core.quit()

    isPractice = expInfo['Practice mode']
    isEEG = expInfo['EEG connected']
    participant = expInfo['Participant number']

    # Make sure participant number is present
    if not participant:
        print("ERROR: Please enter a participant number.")
        core.quit()

    # =========================================================================
    # Date/time
    # =========================================================================

    start_datetime = datetime.now()

    start_date = start_datetime.strftime(
        '%Y-%m-%d'
    )

    start_time = start_datetime.strftime(
        '%H:%M:%S'
    )

    # =========================================================================
    # EEG buttonbox
    # =========================================================================

    if isEEG:

        try:

            from rusocsci import buttonbox

            cc = buttonbox.Buttonbox(
                port='com3'
            )

        except ImportError:

            print(
                "\nERROR: EEG compatibility is designed to work "
                "with the Buttonbox from the rusocsci package.\n"
            )

            core.quit()

    else:

        cc = None

    # =========================================================================
    # Keyboard
    # =========================================================================

    kb = keyboard.Keyboard()

    # =========================================================================
    # Data directory
    # =========================================================================

    data_dir = os.path.join(
        script_dir,
        'data'
    )

    os.makedirs(
        data_dir,
        exist_ok=True
    )

    # =========================================================================
    # Data file
    # =========================================================================

    filename = (
        f"sub-{participant}_"
        f"{'practice' if isPractice else 'task'}.csv"
    )

    data_filename = os.path.join(
        data_dir,
        filename
    )

    datafile = open(
        data_filename,
        'w',
        newline=''
    )

    # =========================================================================
    # Data fields
    # =========================================================================

    fieldnames = [
        'Participant',
        'Practice',
        'EEG',
        'TaskVersion',
        'StartDate',
        'StartTime',
        'StartExperiment',
        'Block',
        'Trial',
        'StartTrial',
        'Animal',
        'Stim1',
        'Stim2',
        'ProbStim1',
        'AmbiguityLevel',
        'Condition',
        'OutcomeIdentity',
        'TrialType',
        'fixation_start_time',
        'fixation_duration',
        'cues_start_time',
        'choice_start_time',
        'outcome_start_time',
        'outcome_duration_time',
        'ITI_start_time',
        'ITI_duration',
        'ButtonPress',
        'StimChosen',
        'StimChosenLabel',
        'RT',
        'OutcomeEvent'
    ]

    writer = csv.DictWriter(
        datafile,
        fieldnames=fieldnames
    )

    writer.writeheader()

    # =========================================================================
    # Experiment data
    # =========================================================================

    expData = {}

    # =========================================================================
    # Window
    # =========================================================================

    win = visual.Window(
        fullscr=True,
        allowGUI=False,
        monitor="testMonitor",
        units='norm',
        color='#656565',
        gammaErrorPolicy="ignore"
    )

    win.mouseVisible = False

    # =========================================================================
    # Run experiment
    # =========================================================================

    try:

        runtrials(
            win=win,
            writer=writer,
            datafile=datafile,
            expData=expData,
            Task="VolatilityLearning",
            participant=participant,
            isPractice=isPractice,
            isEEG=isEEG,
            cc=cc
        )

    except Exception as e:

        print(
            "\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        )

        print("EXPERIMENT ERROR:")
        print(e)

        import traceback
        traceback.print_exc()

        print(
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n"
        )

    finally:

        # Close data file
        if not datafile.closed:
            datafile.close()

        # Close PsychoPy window
        try:
            win.close()
        except Exception:
            pass

        core.quit()