import tkinter as tk
import time
import random
import re

class ExperimentApp:


    def center_window(self):

        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))


    def information_frame_rsvp(self):

        self.information_frame_rsvp = tk.Frame(self.master, bg="white", width=1440, height=1040)
        self.information_frame_rsvp.pack_propagate(False)
        self.information_frame_rsvp.pack(fill="both", expand=True)

        welcome = "Welcome to the first part of this experiment!"
        welcome_label = tk.Label(self.information_frame_rsvp, text=welcome, bg="white", fg="black", font=("Helvetica", 32, "bold"))
        welcome_label.pack(padx=20, pady=20, anchor="center")

        summary = ("For this section, you will be provided with a basic story prompt to read. However,\n"
                    "you will be reading it with a method that uses rapid serial visual processing (RSVP).\n"
                    "The prompt will be flashed on the screen, one word at a time. You are asked to read the\n" 
                    "prompt and to try your best to remember the details, which you will be quizzed on later.\n\n"
                    "Click 'Start' to begin.")
        summary_label = tk.Label(self.information_frame_rsvp, text=summary, bg="white", fg="black", font=("Helvetica", 24))
        summary_label.pack(padx=20, anchor="center")

        start_button = tk.Button(self.information_frame_rsvp, text="Start", command=self.start_reading_frame_rsvp, bg="white", fg="black")
        start_button.pack(pady=20, anchor="center")

        self.center_window()


    def start_reading_frame_rsvp(self):

        self.information_frame_rsvp.destroy()

        pattern = r"Participant (1|2|3|4|5|6|7|8|9)"
        participant_num = 1

        with open("results.txt", "r") as file:
            for line in file:
                match = re.search(pattern, line)
                if match:
                    participant_num = int(match.group(1)) + 1
            
        with open("results.txt", "a") as file:
            file.write("Participant " + str(participant_num) + '\n' + "RSVP Prompt" + '\n')

        self.reading_frame_rsvp("rsvpprompt.txt")
    

    def reading_frame_rsvp(self, file_name):
        
        prompt_rsvp = []
        with open(file_name, 'r') as file:
            for line in file:
                words = line.split()
                for word in words:
                    prompt_rsvp.append(word)
        
        self.text_display = tk.Label(self.master, text="", bg="white", fg="black", font=("Helvetica", 64))
        self.text_display.place(relx=0.5, rely=0.5, anchor="center")
        self.center_window()

        delay_per_word = 60.0 / 400.0  # WPM calculation

        countdown = [ "3", "2", "1", "GO!" ]

        for c in countdown:
            self.text_display.config(text=c)
            self.master.update()
            time.sleep(60.0 / 200.0)

        for word in prompt_rsvp:
            self.text_display.config(text=word)
            self.center_window()
            self.master.update()
            time.sleep(delay_per_word)

        self.master.after(10, lambda: self.start_quiz_rsvp())
    

    def start_quiz_rsvp(self):

        self.text_display.config(text="")
        self.master.update()

        self.current_question_index = 0
        self.quiz_type = "RSVP"
        self.quiz_questions = [
            {
                "question": "Where did Sarah find the kitten initially?",
                "options": ["Home", "Bush", "Bed", "Garage"],
                "correct_answer": "Bush"
            },
            {
                "question": "How old was the kitten?",
                "options": ["1 month", "2 months", "3 months", "4 months"],
                "correct_answer": "4 months"
            },
            {
                "question": "What did Sarah name the kitten?",
                "options": ["Whiskers", "Mittens", "Willie", "Muffin"],
                "correct_answer": "Whiskers"
            }
        ]
        
        self.display_next_question()
    

    def display_next_question(self):

        if self.current_question_index < 3:
            question_data = self.quiz_questions[self.current_question_index]
            self.create_quiz_frame(question_data["question"], question_data["options"], question_data["correct_answer"])
            self.current_question_index += 1
        elif self.quiz_type == "RSVP":
            self.information_frame_static()
        elif self.quiz_type == "Static":
            self.thanks_frame()


    def destroy_quiz_frame(self):

        if hasattr(self, 'quiz_frame'):
            self.quiz_frame.destroy()
            

    def create_quiz_frame(self, question, options, correct_answer):

        self.destroy_quiz_frame()
        
        self.quiz_frame = tk.Frame(self.master, bg="white", width=1440, height=1040)
        self.quiz_frame.pack_propagate(False)
        self.quiz_frame.pack(fill="both", expand=True)

        question_label = tk.Label(self.quiz_frame, text="Answer the following question:", bg="white", fg="black", font=("Helvetica", 14))
        question_label.pack(pady=20)

        question_text = tk.Label(self.quiz_frame, text=question, bg="white", fg="black", font=("Helvetica", 12))
        question_text.pack(pady=10)

        random.shuffle(options)

        selected_option = tk.StringVar()
        for option in options:
            option_button = tk.Radiobutton(self.quiz_frame, text=option, variable=selected_option, value=option, bg="white", fg="black")
            option_button.pack(anchor="w")

        submit_button = tk.Button(self.quiz_frame, text="Submit", command=lambda: self.submit_answer(question, selected_option.get() == correct_answer), bg="white", fg="black")
        submit_button.pack(pady=20)
    

    def submit_answer(self, question, answer):
        
        with open("results.txt", "a") as file:
            file.write(question + ': ' + str(answer) + "\n")

        self.display_next_question()


    def information_frame_static(self):

        self.quiz_frame.destroy()

        self.information_frame_static = tk.Frame(self.master, bg="white", width=1440, height=1040)
        self.information_frame_static.pack_propagate(False)
        self.information_frame_static.pack(fill="both", expand=True)

        welcome = "Welcome to the second part of this experiment!"
        welcome_label = tk.Label(self.information_frame_static, text=welcome, bg="white", fg="black", font=("Helvetica", 32, "bold"))
        welcome_label.pack(padx=20, pady=20, anchor="center")

        summary = ("For this section, you will be provided with a basic story prompt to read. However,\n"
                    "now you will be reading it with a standard static text method along with a time limit.\n"
                    "The prompt will be fully on the screen. You are asked to read this prompt and to try\n" 
                    "your best to remember the details, which you will be quizzed on later.\n\n"
                    "Click 'Start' to begin.")
        summary_label = tk.Label(self.information_frame_static, text=summary, bg="white", fg="black", font=("Helvetica", 24))
        summary_label.pack(padx=20, anchor="center")

        start_button = tk.Button(self.information_frame_static, text="Start", command=self.start_reading_frame_static, bg="white", fg="black")
        start_button.pack(pady=20, anchor="center")

        self.center_window()


    def start_reading_frame_static(self):

        self.information_frame_static.destroy()
            
        with open("results.txt", "a") as file:
            file.write("Static Prompt" + '\n')

        self.reading_frame_static("norsvpprompt.txt")


    def reading_frame_static(self, file_name):

        prompt_static = []
        with open(file_name, 'r') as file:
            for line in file:
                words = line.split()
                for word in words:
                    prompt_static.append(word)

        count = len(prompt_static)

        iterations = 0
        prompt_formatted = []
        for word in prompt_static:
            if iterations % 9 == 0:
                prompt_formatted.append('\n')

            prompt_formatted.append(word)
            iterations += 1

        
        self.text_display = tk.Label(self.master, text="", bg="white", fg="black", font=("Helvetica", 32))
        self.text_display.place(relx=0.5, rely=0.5, anchor="center")
        self.center_window()

        countdown = [ "3", "2", "1", "GO!" ]

        for c in countdown:
            self.text_display.config(text=c)
            self.master.update()
            time.sleep(60.0 / 200.0)

        self.text_display.config(text=" ".join(prompt_formatted))
        self.center_window()
        self.master.update()
        time.sleep(count / 200 * 60)

        self.master.after(10, lambda: self.start_quiz_static())


    def start_quiz_static(self):

        self.text_display.config(text="")
        self.master.update()

        self.current_question_index = 0
        self.quiz_type = "Static"
        self.quiz_questions = [
            {
                "question": "What was the main character's name?",
                "options":  ["Timmy", "Joey", "Bobby", "Henry"],
                "correct_answer": "Timmy"
            },
            {
                "question": "What were their initial emotions upon meeting?",
                "options":  ["Fear", "Surprise", "Anger", "Disgust"],
                "correct_answer": "Fear"
            },
            {
                "question": "What did the alien give to him?",
                "options": ["Crystal", "Teleporter", "Jewel", "Time machine"],
                "correct_answer": "Crystal"
            }
        ]
        
        self.display_next_question()


    def thanks_frame(self):

        self.quiz_frame.destroy()

        with open("results.txt", "a") as file:
            file.write('\n')
        
        self.thanks_frame = tk.Frame(self.master, bg="green", width=1440, height=1040)
        self.thanks_frame.pack_propagate(False)
        self.thanks_frame.pack(fill="both", expand=True)

        self.thanks_display = tk.Label(self.master, text="Thanks for your\nparticipation!", bg="green", fg="white", font=("Helvetica", 32))
        self.thanks_display.place(relx=0.5, rely=0.5, anchor="center")
        self.center_window()


    def __init__(self, master):

        self.master = master
        self.master.title("Experiment")
        self.master.configure(bg="white")
        self.information_frame_rsvp()


if __name__ == "__main__":

    root = tk.Tk()
    app = ExperimentApp(root)
    root.geometry("1440x1040")
    root.mainloop()