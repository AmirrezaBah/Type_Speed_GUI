import tkinter as tk
from functools import partial
from tkinter import  messagebox
import random

#Constants
ROOT_COLOR = '#C7D9DD'
TEXT_AREA_COLOR = '#EEF1DA'
ENTRY_COLOR = '#EEF1DA'
TEXT_AREA_FONT = ('Courier', 20, 'bold')
FONT_COLOR = '#ADB2D4'
LABEL_FONT = ('Courier', 14, 'bold')
BUTTON_COLOR = '#ADB2D4'
BUTTON_FONT = ('Courier', 12, 'bold')
START_BUTTON_COLOR = '#0f9f1a'
RESTART_BUTTON_COLOR = '#9F0F0F'
USER_ENTRY_FONT = ('Courier', 20, 'bold')
CORRECT_TYPED_COLOR = '#0096FF'
FALSE_TYPED_COLOR = '#D70040'
TIMER_FONT = ('Courier', 20, 'bold')

#Global Scope Variable
words_list = None
time_left = 60
after_id = None
index_to_check = 0
total_inputs = 0
correct_typed = 0
total_num_of_characters = 0

#Get Highest Score (Set a File is Not Found, Setting the Highest Score to Average WPM of 40 / Min (Brut))
#And Net to 33 / Min (Second Line)
try:
    with open('scores.txt') as score_file_opened:
        scores = score_file_opened.readlines()
        highest_brut_wpm = int(scores[0])
        highest_net_wpm = int(scores[1])
except FileNotFoundError:
    with open('scores.txt', 'w') as score_file_opened:
        score_file_opened.write('40\n'
                                '33')
        highest_brut_wpm = 40
        highest_net_wpm = 33


#Highlight Current Word Function, Advance Highlighter by Press of Space Bar, Check if User Typed Correctly
def highlight_word(event):
    global index_to_check, total_inputs, correct_typed
    #If User Reaches the End of the Words List:
    if words_list is not None and isinstance(words_list, list):
        if index_to_check == len(words_list):
            root.quit()
            messagebox.showinfo(title='You Completed the Challenge',
                                message='You Bested the Challenge. Congratulations!')
            return
        ###
        #Highlight Word to Type
        text_area.config(state = 'normal')
        query = words_list[index_to_check].strip()
        text_area.tag_remove("highlight", "1.0", tk.END)
        index = text_area.search(query, "1.0", tk.END)
        end_index = f"{index}+{len(query)}c"
        text_area.tag_add("highlight", index, end_index)
        text_area.tag_config("highlight", background="#1fd92d")
        ###
        #Make Sure the Word is Visible in the Viewpoint of the Text Area
        text_area.see( index = index)
        ###
        #Disable Text-Area
        text_area.config(state = 'disabled')
        ###
        #If the Event is Triggered by Space Bar, Check word Typed by User with Reference
        if event is not None:
            #Make the words appear Blue or Red (If they are Typed Correctly or Not)
            word_to_check_index = index_to_check - 1
            user_input = entry_user.get().strip().lower()
            word_to_check = words_list[word_to_check_index].strip()
            fill_index = text_area.search(word_to_check, "1.0", tk.END)
            end_fill_index = f"{fill_index}+{len(word_to_check)}c"
            if user_input == word_to_check:
                correct_typed += 1
                text_area.tag_add(f"fill {fill_index}", fill_index, end_fill_index)
                text_area.tag_config(f"fill {fill_index}", foreground=CORRECT_TYPED_COLOR)
                #Increase Num on Correct Typed Entry
                words_typed_correctly_entry.config(state = 'normal')
                words_typed_correctly_entry.delete(0, 'end')
                words_typed_correctly_entry.insert('end', correct_typed)
                words_typed_correctly_entry.config(state = 'disabled')
                ###
            else:
                text_area.tag_add("fill", fill_index, end_fill_index)
                text_area.tag_config("fill", foreground=FALSE_TYPED_COLOR)
            ###
        ###
            #Clear the User Entry Box After Each Space
            entry_user.delete(0, 'end')
            ###
            #Add to the Total Num of User Inputs and Increment the Index
            index_to_check += 1
            total_inputs += 1
            ###
        else:
            pass
    else:
        return

#Open and Read from words_to_type_english.txt / Create words_list
def open_words_file(language):
    global words_list, index_to_check
    text_area.config(state = 'normal')
    if words_list is None and time_left == 60:
        text_area.delete('1.0', 'end')
        if language == 'EN':
            with open('words_to_type_english.txt', encoding = 'UTF-8') as lan_file_opened:
                words_list = lan_file_opened.readlines()
        else:
            with open('words_to_type_french.txt', encoding = 'UTF-8') as lan_file_opened:
                words_list = lan_file_opened.readlines()
    elif words_list is not None:
        messagebox.showerror(title = 'Language Already Set for This Round',
                             message = 'Language has Already been Chosen for this Round. '
                                       'Please Restart if You Wish To Change.')
        return
    else:
        messagebox.showerror(title = 'Round Already Began',
                             message = 'Round has Already Began. Please Restart First.')
        return
    words_list = [f'{word.split()[0].lower()} ' for word in words_list]
    random.shuffle(words_list)
    for word in words_list:
        text_area.insert('end', word)
    highlight_word(event = None)
    index_to_check += 1
    text_area.config(state = 'disabled')

#Restart Function
def restart():
    global words_list, time_left, after_id, index_to_check, total_num_of_characters, correct_typed, total_inputs
    #Stop Time Count After Restart is Pressed mid-game
    if after_id is not None:
        root.after_cancel(after_id)
    #Show Error if Trying to Restart Without Starting a Round
    if words_list is None:
        messagebox.showerror(title='Game Not Started',
                             message='Please Start a Round First.')
    #Restart Text Area
    text_area.config(state='normal')
    text_area.delete('1.0', 'end')
    text_area.insert('end', 'Words Will Appear Here 👋')
    text_area.config(state='disabled')
    ###
    #Restart Constats
    words_list = None
    time_left = 60
    index_to_check = 0
    total_num_of_characters = 0
    correct_typed = 0
    total_inputs = 0
    after_id = None
    ###
    #Restart Timer
    time_left_entry.config(state='normal')
    time_left_entry.delete(0, 'end')
    time_left_entry.insert('end', time_left)
    time_left_entry.config(state='readonly')
    ###
    #Re-enable Start Button
    start_button.config(state='normal')
    ###
    #Restart Accuracy PCT
    accuracy_pct_entry.delete(0, 'end')
    accuracy_pct_entry.insert('end', f'{0} %')
    accuracy_pct_entry.config(state = 'disabled')
    ###
    #Restart Correct Types
    words_typed_correctly_entry.config(state = 'normal')
    words_typed_correctly_entry.delete(0, 'end')
    words_typed_correctly_entry.insert('end', correct_typed)
    words_typed_correctly_entry.config(state = 'disabled')
    ###
    #Disable Highest Score Entry
    highest_score_entry.config(state = 'readonly')
    ###
    #Disable User Entry
    entry_user.config(state = 'disabled')

#Root Object (Window)
root = tk.Tk()
root.title('Typing Speed Test GUI')
root.config(bg = ROOT_COLOR, padx = 20, pady = 20)

#Text Area (Where the Text to Type will be Shown)
text_area = tk.Text(root, bg = TEXT_AREA_COLOR, font = TEXT_AREA_FONT,
                    relief = 'sunken', width = 30, height = 10, pady = 30, padx = 30,
                    wrap = 'word')
text_area.insert('end', 'Words Will Appear Here 👋')
text_area.config(state = 'disabled')
text_area.grid(column = 0, row = 0, rowspan = 4, padx = 10, pady = 10)

#Entry Widget Label
entry_label = tk.Label(root, text = 'Type Here:',
                       font = LABEL_FONT, bg = ROOT_COLOR)
entry_label.grid(column = 0, row = 4, padx = 10, pady = 10)

#Entry Widget (User Type) (Disabled Until User Clicks on Start. After, Insertion Cursor Focuses on it Automatically)
entry_user = tk.Entry(root, width = 40, bg = ENTRY_COLOR, state = 'disabled', font = USER_ENTRY_FONT)
entry_user.grid(column = 0, row = 5, padx = 10, pady = 10)

#Timer Label
time_left_label = tk.Label(root, text = 'Time Left:', bg = ROOT_COLOR, font = LABEL_FONT)
time_left_label.grid(column = 1, row = 0, padx = 10, pady = 10, sticky = 'w')

#Timer Entry (Read Only)
time_left_entry = tk.Entry(root, width = 8,
                           border = 0, highlightthickness = 0, font = TIMER_FONT,
                           justify = 'center')
time_left_entry.insert('end', 60)
time_left_entry.config(state = 'readonly')
time_left_entry.grid(column = 2, row = 0, sticky = 'e', padx = 10, pady = 10)

#Time Countdown Function
def time_count_down():
    global time_left, after_id
    # When Time Count down has Started (by Pressing the Start Button) and a Language Has been Chosen
    if time_left > 0 and words_list is not None:
        entry_user.config(state='normal')
        entry_user.focus_set()
        time_left -= 1
        time_left_entry.config(state='normal')
        time_left_entry.delete(0, 'end')
        time_left_entry.insert('end', str(time_left))
        time_left_entry.config(state='readonly')
        start_button.config(state = 'disabled')
        after_id = root.after(1000, time_count_down)
    #When Time is Up:
    elif time_left == 0:
        try:
            #Calculating Accuracy on a Word-on-Word Basis
            accuracy_pct = round((correct_typed / total_inputs) * 100, 2)
        except ZeroDivisionError:
            #If User Entered no Data:
            messagebox.showerror(title='No Data Entered',
                                 message = 'No Data Was Entered.')
            return
        #Displaying User Stats:
        #Accuracu PCT:
        accuracy_pct_entry.config(state = 'normal')
        accuracy_pct_entry.delete(0, 'end')
        accuracy_pct_entry.insert('end', f'{accuracy_pct} %')
        words_typed_correctly_entry.config(state='disabled')
        ###
        #Cleaning User Entry (If Anything is Left)
        entry_user.delete(0, 'end')
        entry_user.config(state='disabled')
        ###
        #Calculate Brut WPM
        brut_wpm = int((total_num_of_characters / 5) / 2)
        ###
        #Calculate Net WPM
        net_wpm = brut_wpm - (total_inputs - correct_typed)
        ###
        #Replace the Highest Score if the Brut WPM of the Round Surpasses Highest Score Saved Before
        if brut_wpm > highest_brut_wpm:
            #How to Reset scores.txt (If ONLY Brut WPM Beats Highest Brut WPM:)
            with open('scores.txt', 'w') as file:
                file.write(f'{brut_wpm}\n'
                           f'{highest_net_wpm}')
        if net_wpm > highest_net_wpm:
            #How to Reset scores.txt (If ONLY Net WPM Beats Highest Net WPM:)
            with open('scores.txt', 'w') as file:
                file.write(f'{highest_brut_wpm}\n'
                           f'{net_wpm}')
        if net_wpm > highest_net_wpm and brut_wpm > highest_brut_wpm:
            # How to Reset scores.txt (If BOTH Net / Brut WPM Beat Highest Net / Brut WPM:)
            with open('scores.txt', 'w') as file:
                file.write(f'{brut_wpm}\n'
                           f'{net_wpm}')
            #Show in Entry (Highest Score)
            highest_score_entry.config(state = 'normal')
            highest_score_entry.delete(0, 'end')
            highest_score_entry.insert('end', brut_wpm)
            highest_score_entry.config(state = 'disabled')
        else:
            pass
        ###
        #Show Message, Display Stats
        messagebox.showinfo(title="Time's Up!",
                            message=f"1 Min is up. You Achieved\n"
                                    f"Total Num of Words User Typed: {total_inputs}\n"
                                    f"Correct Typed: {correct_typed}\n"
                                    f"Total Num of Characters User Typed: {total_num_of_characters}\n"
                                    f"Accuracy (PCT): {accuracy_pct} %\n"
                                    f"Brut WPM (Words Per Min): {brut_wpm}\n"
                                    f"Net WPM: {net_wpm}")
    #If a Language Has not been Chosen Before Clicking on Start
    else:
        messagebox.showinfo(title='No Language Chosen',
                            message='Please choose a language first.')

#Words Typed Correctly Label
words_typed_correctly = tk.Label(root, text = 'Correct Typed:', font = LABEL_FONT,
                                 bg = ROOT_COLOR)
words_typed_correctly.grid(column = 1, row = 1, padx = 10, pady = 10, sticky = 'w')

#Words Typed Correctly Count (Readonly)
words_typed_correctly_entry = tk.Entry(root,
                                       border = 0, highlightthickness = 0, width = 8)
words_typed_correctly_entry.insert('end', 0)
words_typed_correctly_entry.config(state = 'readonly')

words_typed_correctly_entry.grid(column = 2, row = 1, sticky = 'e', pady = 10, padx = 10)

#Accuracy Percentage Label
accuracy_pct_label = tk.Label(root, text = 'Accuracy (PCT):', bg = ROOT_COLOR,
                              font = LABEL_FONT)
accuracy_pct_label.grid(column = 1, row = 2, sticky = 'w', padx = 10, pady = 10)

#Accuracy Percentage Entry (Readonly)
accuracy_pct_entry = tk.Entry(root, width = 8, border = 0, highlightthickness = 0)
accuracy_pct_entry.insert('end', f'{0} %')
accuracy_pct_entry.config(state = 'readonly')
accuracy_pct_entry.grid(column = 2, row = 2, sticky = 'e', pady = 10, padx = 10)

#Highest Score Label
highest_score_label = tk.Label(root, text = 'Highest Score (Brut WPM):', font = LABEL_FONT,
                               bg = ROOT_COLOR)
highest_score_label.grid(column = 1, row = 3,sticky = 'w', padx = 10, pady = 10)

#Highest Score Entry (Readonly)
highest_score_entry = tk.Entry(root, width = 8, border = 0,
                               highlightthickness = 0)
highest_score_entry.insert('end', highest_brut_wpm)
highest_score_entry.config(state = 'readonly')
highest_score_entry.grid(column = 2, row = 3,sticky = 'e', padx = 10, pady = 10)

#Language Label
language_label = tk.Label(root, text = 'Language:', bg= ROOT_COLOR,
                          font = LABEL_FONT)
language_label.grid(column = 1, row = 4, pady = 10, padx = 10, sticky = 'w')

#English Button
english_button = tk.Button(root, text = 'English', bg = BUTTON_COLOR, relief = 'raised', width = 6,
                           command = partial(open_words_file, 'EN'))
english_button.grid(column=2, row= 4, sticky = 'e', pady = 10, padx = 10)

#French Button
french_button = tk.Button(root, text = 'Français', bg = BUTTON_COLOR, relief = 'raised', width = 6,
                          command = partial(open_words_file, 'FR'))
french_button.grid(column=2, row= 5, sticky = 'e', pady = 10, padx = 10)

#Start Button (Disabled During a Round)
start_button = tk.Button(root, text = 'Start', font = BUTTON_FONT,
                         bg = START_BUTTON_COLOR, relief = 'raised',
                         command = time_count_down)
start_button.grid(column = 1, row = 6)

#Restart Button
restart_button = tk.Button(root, text = 'Restart', font = BUTTON_FONT,
                         bg = RESTART_BUTTON_COLOR, relief = 'raised', command = restart)
restart_button.grid(column = 2, row = 6)

#Char Counter (To Calculate Brut WPM)
def char_counter(event):
    global total_num_of_characters
    if event.char.isalpha():
        total_num_of_characters += 1
    else:
        pass

#Binding Space Key to Moving Highlighter
root.bind('<space>', highlight_word)

#Binding Total Num of Characters Counter to Any Key Press
root.bind('<Key>', char_counter)


root.mainloop()