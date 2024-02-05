import random
import nltk
import json
import tkinter as tk
from tkinter import scrolledtext
from tkinter import simpledialog
from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.optimizers import SGD
from keras.layers import Dense, Activation, Dropout
from keras.models import load_model
import numpy as np
from spellchecker import SpellChecker
import pickle
body_feature_mappings = {
    'Frame': {'slim unusually tall or short': 1, 'medium athletic': 2, 'large body rounded curves': 3},
    'weight': {'lose easily': 1, 'if gains weight around the middle fairly stable ': 2, 'deposits fat fairly evenly gains easily, especially rear & thighs': 3},
    'Chin': {'thin delicate angular': 1, 'moderate tapering': 2, 'large jaw rounded, double': 3},
    'Weight in your childhood':{'thin as a child':1,'medium Build as a child':2,'large or chunky as a child':3},
    'Eyes':{'small sunken dark, active':1,'medium grey green yellow red blue':2,'big loving blue chocolate brown':3},
    'Nose':{'uneven shape deviated septum':1,'long, pointed red nose tip':2,'short rounded button nose':3},
    'Body hair':{'scanty or excessive dark coarse curly':1,'light body hair fine texture':2,'moderate amount of body hair':3},
    'teeth':{'stick out big roomy thin,gums sensitivity':1,'medium even soft tender gums':2,'large even white gleeming':3},
    'Complexion':{'dark complexion tans easy':1,'fair skin burns easy freckles moles common':2,'tans evenly':3},
    'Hair':{'kinky curly brown black scarce':1,'straight fine light red coloured':2,'thick wavy luxurient':3},
    'Hands':{'long tapering fingers and toes':1,'fingers and toes medium in length':2,'fingers and toes short and squarish':3},
    'Neck':{'thin tall unsteady':1,'moderate medium':2,'big folded steady':3},
    'Forehead':{'small forehead':1,'medium with folds and lines:':2,'large forehead':3},
    '00Belly button':{'small irregular herniated':1,'oval superficial':2,'big, deep round stretched':3},
    'Hips':{'slender thin':1,'moderate':2,'heavy big':3},
    'Bones':{'light small bones prominent joints':1,'moderate':2,'heavy bone structure':3},
    'Bowels':{'irregular appetite tendency to constipation':1,'strong appetite tendency to lose stool':2,'Low but constant thick stools':3}}

intents_mind={
    'Mental activity':{'hyperactive short term concentration purposeful':1, 'logical rational':2,'slow paced consistent':3},
    'Habits':{'travel art dance trivia':1,'intense sports debates politics hunting research':2,'sailing flowers business cosmetics cooking':3},
    'Recollection':{'recent good forgets easily':1,'distinct memory often visual':2,'slow to learn but sustained memory':3},
    'Routine':{'dislikes routine':1,'enjoy planning organising self created':2,'works well with routine':3},
    'Decisions':{'indecisive changes mind easily':1,'rapid decision making sees things clearly':2,'slow to decide commits once chosen Prefers to follow a plan':3},
    'Thinking':{'creative thinker can get many ideas':1,'organised thinker entrepreneurial':2,'prefers to follow plan':3},
    'Projects':{'many at once, often does not finish':1,'organised and logical goal focused':2,'resists change likes simplicity':3},
    'Financial':{'spends impusively':1,'spends on luxuries spends on achieving purpose':2,'wealthy good money preserver':3},
    'physical activity':{'hyperactive lots of movement':1,'purposeful for reason':2,'slow calm':3},
    'sexual desire':{'strong desires fantasy but low energy':1,'moderate desire passionate dominating':2,'consistent desire loving nurturing':3}}

class Prakriti_Chatbot:
    def scroll_to_bottom(self):
        self.chat_history.yview_moveto(1.0)

    def initialize_chatbot(self,root):
        self.root=root
        self.spell_checker = SpellChecker() 
        self.chat_history = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=40, height=10)
        self.chat_history.grid(column=0, row=0, padx=10, pady=10, columnspan=3)

        self.user_input_entry = tk.Entry(self.root, width=40)
        self.user_input_entry.grid(column=0, row=1, padx=10, pady=10)

        self.send_button = tk.Button(self.root, text="Proceed", command=self.process_user_input)
        self.send_button.grid(column=1, row=1, padx=10, pady=10)

        self.greet_inputs = ['hello', 'hi', 'sup', 'hey']
        self.greet_responses = ['hi', 'hey!!', 'hi there', 'hello', 'I am glad! You are talking to me']

        self.chat_history.insert(tk.END, "Chatbot: Hello there! I am a chatbot here to talk about Prakriti body types...\n")
        self.chat_history.insert(tk.END, "Chatbot: To get started, I'll ask you some questions about your body and mind... Type start to continue...\n")

    def process_user_input(self):
        user_input = self.user_input_entry.get().lower()
        self.user_input_entry.delete(0, tk.END)

        if user_input in self.greet_inputs:
            response = random.choice(self.greet_responses)
            self.chat_history.insert(tk.END, f'User: {user_input}\n')
            self.chat_history.insert(tk.END, f'Chatbot: {response}\n')
        elif user_input == 'start':
            self.evaluate_input()

    def evaluate_input(self):
        type1 = type2 = type3 = 0
        
        for y in [body_feature_mappings, intents_mind]:
            for feature, feature_values in y.items():
                x=0
                while x==0:
                    a = {}
                    print(f'Chatbot: Tell your {feature}')
                    for value in feature_values:
                        self.chat_history.insert(tk.END, f'BOT: {feature_values[value]}  {value}\n')
                        a[value] = feature_values[value]
                    self.scroll_to_bottom()
                    user_input=simpledialog.askstring("Input", f"Tell your {feature}:")
                             # Spell check and correction
                    self.chat_history.insert(tk.END, f'User: {user_input}\n')
                    r_input=''
                    print(user_input)
                    if user_input.isdigit():
                        if int(user_input)==1:
                            type1+=1;x=1
                        elif int(user_input)==2:
                            type2+=1;x=1
                        elif int(user_input)==3:
                            type3+=1;x=1
                    elif a:
                        for word in user_input.split():
                            corrected_word = self.spell_checker.correction(word)
                            r_input += corrected_word + " "
                        for value, score in a.items():
                            d = e = c = 0

                            for z in r_input.split():
                                
                                z=z.lower()
                                if z in value.lower():
                                    p = score
                                    print(score)
                                    if p == 1:
                                        d += 1
                                    elif p == 2:
                                        e += 1
                                    elif p == 3:
                                        c += 1

                            if d > e and d > c:
                                type1 += 1
                                x = 1
                                print('add')
                            elif e > d and e > c:
                                type2 += 1
                                x = 1
                                print('add2')
                            elif c > d and c > e:
                                type3 += 1
                                x = 1
                                print('add3')
                    
                    self.chat_history.insert(tk.END, f'BOT: {type1, type2, type3}\n')
                    self.chat_history.insert(tk.END,'-' * 40)
                    if x==0:
                        self.chat_history.insert(tk.END,'BOT: your input does not match please try again\n')
        self.scroll_to_bottom()        
        self.chat_history.insert(tk.END, f'BOT: {type1, type2, type3}\n')
        m = np.max([type1, type2, type3])
        if m == type1:
            category_input = 'vata'
            self.chat_history.insert(tk.END,'Chatbot: YOUR BODYTYPE IS VATA \n')
            print('Chatbot: YOUR BODYTYPE IS VATA')
        elif m == type2:
            category_input = 'pitta'
            self.chat_history.insert(tk.END,'Chatbot: YOUR BODYTYPE IS PITTA\n')
            print('Chatbot: YOUR BODYTYPE IS PITTA')
        elif m == type3:
            category_input = 'kapha'
            self.chat_history.insert(tk.END,'Chatbot: YOUR BODYTYPE IS KAPHA\n')
            print('Chatbot: YOUR BODYTYPE IS KAPHA')
        print('-' * 100)
        food_preferences = {
            'vata': {
                'general': ['food in small quantities', 'ginger', 'garlic'],
                'cereals': ['wheat', 'sesame'],
                'pulses': ['black gram', 'green gram'],
                'milk products': ['curd', 'ghee', 'butter', 'cheese'],
                'oils': ['sesame oil', 'castor oil', 'cod liver oil'],
                'vegetables': ['white gourd', 'drumstick', 'onion', 'asparagus', 'radish'],
                'fruits': ['mango', 'coconut', 'grapes', 'dates', 'pineapple', 'almonds', 'figs']
            },
            'pitta': {
                'general': ['cold', 'dry', 'sweet', 'bitter'],
                'cereals': ['wheat', 'barley'],
                'pulses': ['masur', 'greengram', 'channa'],
                'veggies': ['snake gourd', 'white gourd', 'carrot', 'beetroot'],
                'fruit': ['dried grapes', 'apple', 'pomegranate', 'ripe bananas'],
                'spices': ['coriander', 'rock salt'],
                'meat': ['deer', 'goat']
            },
            'kapha': {
                'general': ['light', 'hot', 'dry', 'pungent'],
                'cereals': ['barley'],
                'pulses': ['masur', 'horse gram', 'green gram'],
                'oils': ['mustard oil', 'sesame oil'],
                'veggies': ['bitter gourd', 'drumstick', 'snake gourd', 'onions'],
                'fruit': ['pomegranates', 'lemon'],
                'spices': ['dry ginger', 'black cumin seeds', 'garlic', 'pepper'],
                'other': ['old wine', 'honey']
            }
        }
        ''''''
        print('-'*100)
        print('FOOD PREFERENCES FOR ', category_input.upper())
        print('-'*100)
        #self.chat_history.insert(tk.END,)
        def print_food_preferences(category):
            if category in food_preferences:
                for group, items in food_preferences[category].items():
                    if group == 'general':
                        self.chat_history.insert(tk.END,'General:'+', '.join(items)+'\n')
                        print('General:'+ ', '.join(items))
                    else:
                        self.chat_history.insert(tk.END,f'{group.capitalize()}:'+', '.join(items)+'\n')
                        print(f'{group.capitalize()}:', ', '.join(items))
            else:
                print(f'Category "{category}" not found in food preferences.')
                self.chat_history.insert(tk.END,f'Category "{category}" not found in food preferences.')
                                         
        print_food_preferences(category_input)
        print('-'*100, '\n')
        self.chat_history.insert(tk.END,'-' * 40)
        life_style = {
            'communication': {'talkative': 'vata', 'sharp': 'pitta', 'incisive': 'pitta', 'communication with analytical abilities': 'pitta', 'less vocal': 'kapha', 'with good communication skills': 'kapha'},
            'Memory': {'quick': 'vata', 'grasping but poor retention': 'vata', 'Moderate': 'pitta', 'Grasping retention': 'pitta', 'slow': 'kapha', 'grasping but good retention': 'kapha'},
            'Initiation_Capabilities': {'quick': 'vata', 'responsive': 'vata', 'moderate': 'pitta', 'understanding': 'pitta', 'slow': 'kapha'},
            'Emotional_Temperature': {'fearful': 'vata', 'moody': 'vata', 'unpredictable': 'vata', 'aggressive': 'pitta', 'jealous': 'pitta', 'impatience': 'pitta', 'calm': 'kapha', 'attached': 'kapha', 'likeable': 'kapha'},
            'Pulse': {'thready': 'vata', 'feeble': 'vata', 'moves like a snake': 'vata', 'moderate': 'pitta', 'jumping like a frog': 'pitta', 'slow': 'kapha', 'moves like a swan': 'kapha'}
#the idea save all recieved inputs in a list if anything gone wrong recurse it and apply saved 
        }
        print('-'*100)
        print('LIFESTYLE PREFERENCES FOR ', category_input.upper())
        print('-'*100)
        def print_keys_and_values_by_value(value):
            found = False
            for key, val_dict in life_style.items():
                if value in val_dict.values():
                    found = True
                    matching_keys = [k for k, v in val_dict.items() if v == value]
                    for matching_key in matching_keys:
                        self.chat_history.insert(tk.END,f"Bot:  {key}-{matching_key}\n")
                        print(f"{key}-{matching_key}")
            if not found:
                print(f'No keys found with value {value}.')
        print_keys_and_values_by_value(category_input)
        print('-'*100)
        self.chat_history.insert(tk.END,'-' * 40)
        return[type1,type2,type3]

        # Rest of your code...

        return [type1, type2, type3]

# Main function
def main_function():
    root = tk.Tk()
    chatbot_instance = Prakriti_Chatbot()
    chatbot_instance.initialize_chatbot(root)

    # Additional code or logic

    root.mainloop()

# Call the main function
lemmatizer = WordNetLemmatizer()

words = pickle.load(open('word_list.pkl', 'rb'))#
classes = pickle.load(open('classes.pkl', 'rb'))#
model = load_model('chatbot.h5')
intents = json.loads(open('intents.json').read())
def clear_sentence(sentence):
    'tokenize'
    sentence_word = nltk.word_tokenize(sentence)
    sentence_word = [lemmatizer.lemmatize(word) for word in sentence_word]
    return sentence_word

def bag(sentence):
    'checks how many words present in data'
    a = clear_sentence(sentence)
    bag = [0] * len(words)
    for w in a:
        if w in words:
            bag[words.index(w)] = 1
    return np.array(bag)

def predict(sentence):
    'predicts the output based on input but if given unknown word its giving hello :('
    bow = bag(sentence)
    print(bow)
    bow = bow.reshape(1, -1)  # Reshape to match the model input shape
    print(bow)
    if 1 not in bow:
        return -1
    res = model.predict(bow)[0]
    ERROR_THRESHOLD = 0.25
    ress = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    ress.sort(key=lambda x: x[1], reverse=True)
    ret = []
    for a in ress:
        ret.append({'intent': classes[a[0]], 'probability': str(a[1])})
    return ret

def get_resp(intentss_list, intents_json):
    'goes into data to check for responses'
    tag = intentss_list[0]['intent']
    list_of_intentss = intents_json['intents']
    for i in list_of_intentss:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

while True:
    if "pakruti" in classes:
        print('yesss')
    user_input = input('')
    pred = predict(user_input)
    print(pred)
    if pred==-1:
        print('sry,i didnt catch you')
        continue
    response = get_resp(pred, intents)
    print(response)
    if response=='sure':
        print('still should write')
        main_function()







'''
body_feature_mappings = {
    'Frame': {'slim unusually tall or short': 1, 'medium athletic': 2, 'large body rounded curves': 3},
    'weight': {'lose easily': 1, 'if gains weight around the middle fairly stable ': 2, 'deposits fat fairly evenly gains easily, especially rear & thighs': 3},
    'Chin': {'thin delicate angular': 1, 'moderate tapering': 2, 'large jaw rounded, double': 3},
    'Weight in your childhood':{'thin as a child':1,'medium Build as a child':2,'large or chunky as a child':3},
    'Eyes':{'small sunken dark, active':1,'medium grey green yellow red blue':2,'big loving blue chocolate brown':3},
    'Nose':{'uneven shape deviated septum':1,'long, pointed red nose tip':2,'short rounded button nose':3},
    'Body hair':{'scanty or excessive dark coarse curly':1,'light body hair fine texture':2,'moderate amount of body hair':3},
    'teeth':{'stick out big roomy thin,gums sensitivity':1,'medium even soft tender gums':2,'large even white gleeming':3},
    'Complexion':{'dark complexion tans easy':1,'fair skin burns easy freckles moles common':2,'tans evenly':3},
    'Hair':{'kinky curly brown black scarce':1,'straight fine light red coloured':2,'thick wavy luxurient':3},
    'Hands':{'long tapering fingers and toes':1,'fingers and toes medium in length':2,'fingers and toes short and squarish':3},
    'Neck':{'thin tall unsteady':1,'moderate medium':2,'big folded steady':3},
    'Forehead':{'small forehead':1,'medium with folds and lines:':2,'large forehead':3},
    '00Belly button':{'small irregular herniated':1,'oval superficial':2,'big, deep round stretched':3},
    'Hips':{'slender thin':1,'moderate':2,'heavy big':3},
    'Bones':{'light small bones prominent joints':1,'moderate':2,'heavy bone structure':3},
    'Bowels':{'irregular appetite tendency to constipation':1,'strong appetite tendency to lose stool':2,'Low but constant thick stools':3}}

intents_mind={
    'Mental activity':{'hyperactive short term concentration purposeful':1, 'logical rational':2,'slow paced consistent':3},
    'Habits':{'travel art dance trivia':1,'intense sports debates politics hunting research':2,'sailing flowers business cosmetics cooking':3},
    'Recollection':{'recent good forgets easily':1,'distinct memory often visual':2,'slow to learn but sustained memory':3},
    'Routine':{'dislikes routine':1,'enjoy planning organising self created':2,'works well with routine':3},
    'Decisions':{'indecisive changes mind easily':1,'rapid decision making sees things clearly':2,'slow to decide commits once chosen Prefers to follow a plan':3},
    'Thinking':{'creative thinker can get many ideas':1,'organised thinker entrepreneurial':2,'prefers to follow plan':3},
    'Projects':{'many at once, often does not finish':1,'organised and logical goal focused':2,'resists change likes simplicity':3},
    'Financial':{'spends impusively':1,'spends on luxuries spends on achieving purpose':2,'wealthy good money preserver':3},
    'physical activity':{'hyperactive lots of movement':1,'purposeful for reason':2,'slow calm':3},
    'sexual desire':{'strong desires fantasy but low energy':1,'moderate desire passionate dominating':2,'consistent desire loving nurturing':3}}

class Prakriti_Chatbot:
    def scroll_to_bottom(self):
        self.chat_history.yview_moveto(1.0)
    def __init__(self, root):
        self.root = root
        root.title("Prakriti Chatbot")
        self.spell_checker = SpellChecker() 
        self.chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.chat_history.grid(column=0, row=0, padx=10, pady=10, columnspan=3)

        self.user_input_entry = tk.Entry(root, width=40)
        self.user_input_entry.grid(column=0, row=1, padx=10, pady=10)

        self.send_button = tk.Button(root, text="Proceed", command=self.process_user_input)
        self.send_button.grid(column=1, row=1, padx=10, pady=10)

        self.greet_inputs = ['hello', 'hi', 'sup', 'hey']
        self.greet_responses = ['hi', 'hey!!', 'hi there', 'hello', 'I am glad! You are talking to me']

        self.chat_history.insert(tk.END, "Chatbot: Hello there! I am a chatbot here to talk about Prakriti body types...\n")
        self.chat_history.insert(tk.END, "Chatbot: To get started, I'll ask you some questions about your body and mind... Type start to continue...\n")
    def process_user_input(self):
        user_input = self.user_input_entry.get().lower()
        self.user_input_entry.delete(0, tk.END)

        if user_input in self.greet_inputs:
            response = random.choice(self.greet_responses)
            self.chat_history.insert(tk.END, f'User: {user_input}\n')
            self.chat_history.insert(tk.END, f'Chatbot: {response}\n')
        elif user_input=='start':
            response = self.evaluate_input()

    def evaluate_input(self):
        type1 = type2 = type3 = 0
        
        for y in [body_feature_mappings, intents_mind]:
            for feature, feature_values in y.items():
                x=0
                while x==0:
                    a = {}
                    print(f'Chatbot: Tell your {feature}')
                    for value in feature_values:
                        self.chat_history.insert(tk.END, f'BOT: {feature_values[value]}  {value}\n')
                        a[value] = feature_values[value]
                    self.scroll_to_bottom()
                    user_input=simpledialog.askstring("Input", f"Tell your {feature}:")
                             # Spell check and correction
                    self.chat_history.insert(tk.END, f'User: {user_input}\n')
                    r_input=''
                    print(user_input)
                    if user_input.isdigit():
                        if int(user_input)==1:
                            type1+=1;x=1
                        elif int(user_input)==2:
                            type2+=1;x=1
                        elif int(user_input)==3:
                            type3+=1;x=1
                    elif a:
                        for word in user_input.split():
                            corrected_word = self.spell_checker.correction(word)
                            r_input += corrected_word + " "
                        for value, score in a.items():
                            d = e = c = 0

                            for z in r_input.split():
                                
                                z=z.lower()
                                if z in value.lower():
                                    p = score
                                    print(score)
                                    if p == 1:
                                        d += 1
                                    elif p == 2:
                                        e += 1
                                    elif p == 3:
                                        c += 1

                            if d > e and d > c:
                                type1 += 1
                                x = 1
                                print('add')
                            elif e > d and e > c:
                                type2 += 1
                                x = 1
                                print('add2')
                            elif c > d and c > e:
                                type3 += 1
                                x = 1
                                print('add3')
                    
                    self.chat_history.insert(tk.END, f'BOT: {type1, type2, type3}\n')
                    self.chat_history.insert(tk.END,'-' * 40)
                    if x==0:
                        self.chat_history.insert(tk.END,'BOT: your input does not match please try again\n')
        self.scroll_to_bottom()        
        self.chat_history.insert(tk.END, f'BOT: {type1, type2, type3}\n')
        m = np.max([type1, type2, type3])
        if m == type1:
            category_input = 'vata'
            self.chat_history.insert(tk.END,'Chatbot: YOUR BODYTYPE IS VATA \n')
            print('Chatbot: YOUR BODYTYPE IS VATA')
        elif m == type2:
            category_input = 'pitta'
            self.chat_history.insert(tk.END,'Chatbot: YOUR BODYTYPE IS PITTA\n')
            print('Chatbot: YOUR BODYTYPE IS PITTA')
        elif m == type3:
            category_input = 'kapha'
            self.chat_history.insert(tk.END,'Chatbot: YOUR BODYTYPE IS KAPHA\n')
            print('Chatbot: YOUR BODYTYPE IS KAPHA')
        print('-' * 100)
        food_preferences = {
            'vata': {
                'general': ['food in small quantities', 'ginger', 'garlic'],
                'cereals': ['wheat', 'sesame'],
                'pulses': ['black gram', 'green gram'],
                'milk products': ['curd', 'ghee', 'butter', 'cheese'],
                'oils': ['sesame oil', 'castor oil', 'cod liver oil'],
                'vegetables': ['white gourd', 'drumstick', 'onion', 'asparagus', 'radish'],
                'fruits': ['mango', 'coconut', 'grapes', 'dates', 'pineapple', 'almonds', 'figs']
            },
            'pitta': {
                'general': ['cold', 'dry', 'sweet', 'bitter'],
                'cereals': ['wheat', 'barley'],
                'pulses': ['masur', 'greengram', 'channa'],
                'veggies': ['snake gourd', 'white gourd', 'carrot', 'beetroot'],
                'fruit': ['dried grapes', 'apple', 'pomegranate', 'ripe bananas'],
                'spices': ['coriander', 'rock salt'],
                'meat': ['deer', 'goat']
            },
            'kapha': {
                'general': ['light', 'hot', 'dry', 'pungent'],
                'cereals': ['barley'],
                'pulses': ['masur', 'horse gram', 'green gram'],
                'oils': ['mustard oil', 'sesame oil'],
                'veggies': ['bitter gourd', 'drumstick', 'snake gourd', 'onions'],
                'fruit': ['pomegranates', 'lemon'],
                'spices': ['dry ginger', 'black cumin seeds', 'garlic', 'pepper'],
                'other': ['old wine', 'honey']
            }
        }
        print('-'*100)
        print('FOOD PREFERENCES FOR ', category_input.upper())
        print('-'*100)
        #self.chat_history.insert(tk.END,)
        def print_food_preferences(category):
            if category in food_preferences:
                for group, items in food_preferences[category].items():
                    if group == 'general':
                        self.chat_history.insert(tk.END,'General:'+', '.join(items)+'\n')
                        print('General:'+ ', '.join(items))
                    else:
                        self.chat_history.insert(tk.END,f'{group.capitalize()}:'+', '.join(items)+'\n')
                        print(f'{group.capitalize()}:', ', '.join(items))
            else:
                print(f'Category "{category}" not found in food preferences.')
                self.chat_history.insert(tk.END,f'Category "{category}" not found in food preferences.')
                                         
        print_food_preferences(category_input)
        print('-'*100, '\n')
        self.chat_history.insert(tk.END,'-' * 40)
        life_style = {
            'communication': {'talkative': 'vata', 'sharp': 'pitta', 'incisive': 'pitta', 'communication with analytical abilities': 'pitta', 'less vocal': 'kapha', 'with good communication skills': 'kapha'},
            'Memory': {'quick': 'vata', 'grasping but poor retention': 'vata', 'Moderate': 'pitta', 'Grasping retention': 'pitta', 'slow': 'kapha', 'grasping but good retention': 'kapha'},
            'Initiation_Capabilities': {'quick': 'vata', 'responsive': 'vata', 'moderate': 'pitta', 'understanding': 'pitta', 'slow': 'kapha'},
            'Emotional_Temperature': {'fearful': 'vata', 'moody': 'vata', 'unpredictable': 'vata', 'aggressive': 'pitta', 'jealous': 'pitta', 'impatience': 'pitta', 'calm': 'kapha', 'attached': 'kapha', 'likeable': 'kapha'},
            'Pulse': {'thready': 'vata', 'feeble': 'vata', 'moves like a snake': 'vata', 'moderate': 'pitta', 'jumping like a frog': 'pitta', 'slow': 'kapha', 'moves like a swan': 'kapha'}
#the idea save all recieved inputs in a list if anything gone wrong recurse it and apply saved 
        }
        print('-'*100)
        print('LIFESTYLE PREFERENCES FOR ', category_input.upper())
        print('-'*100)
        def print_keys_and_values_by_value(value):
            found = False
            for key, val_dict in life_style.items():
                if value in val_dict.values():
                    found = True
                    matching_keys = [k for k, v in val_dict.items() if v == value]
                    for matching_key in matching_keys:
                        self.chat_history.insert(tk.END,f"Bot:  {key}-{matching_key}\n")
                        print(f"{key}-{matching_key}")
            if not found:
                print(f'No keys found with value {value}.')
        print_keys_and_values_by_value(category_input)
        print('-'*100)
        self.chat_history.insert(tk.END,'-' * 40)
        return[type1,type2,type3]'''











'''
body_feature_mappings = {
    'Frame': {'slim unusually tall or short': 1, 'medium athletic': 2, 'large body rounded curves': 3},
    'weight': {'lose easily': 1, 'if gains weight around the middle fairly stable ': 2, 'deposits fat fairly evenly gains easily, especially rear & thighs': 3},
    'Chin': {'thin delicate angular': 1, 'moderate tapering': 2, 'large jaw rounded, double': 3},
    'Weight in your childhood':{'thin as a child':1,'medium Build as a child':2,'large or chunky as a child':3},
    'Eyes':{'small sunken dark, active':1,'medium grey green yellow red blue':2,'big loving blue chocolate brown':3},
    'Nose':{'uneven shape deviated septum':1,'long, pointed red nose tip':2,'short rounded button nose':3},
    'Body hair':{'scanty or excessive dark coarse curly':1,'light body hair fine texture':2,'moderate amount of body hair':3},
    'teeth':{'stick out big roomy thin,gums sensitivity':1,'medium even soft tender gums':2,'large even white gleeming':3},
    'Complexion':{'dark complexion tans easy':1,'fair skin burns easy freckles moles common':2,'tans evenly':3},
    'Hair':{'kinky curly brown black scarce':1,'straight fine light red coloured':2,'thick wavy luxurient':3},
    'Hands':{'long tapering fingers and toes':1,'fingers and toes medium in length':2,'fingers and toes short and squarish':3},
    'Neck':{'thin tall unsteady':1,'moderate medium':2,'big folded steady':3},
    'Forehead':{'small forehead':1,'medium with folds and lines:':2,'large forehead':3},
    '00Belly button':{'small irregular herniated':1,'oval superficial':2,'big, deep round stretched':3},
    'Hips':{'slender thin':1,'moderate':2,'heavy big':3},
    'Bones':{'light small bones prominent joints':1,'moderate':2,'heavy bone structure':3},
    'Bowels':{'irregular appetite tendency to constipation':1,'strong appetite tendency to lose stool':2,'Low but constant thick stools':3}}

intents_mind={
    'Mental activity':{'hyperactive short term concentration purposeful':1, 'logical rational':2,'slow paced consistent':3},
    'Habits':{'travel art dance trivia':1,'intense sports debates politics hunting research':2,'sailing flowers business cosmetics cooking':3},
    'Recollection':{'recent good forgets easily':1,'distinct memory often visual':2,'slow to learn but sustained memory':3},
    'Routine':{'dislikes routine':1,'enjoy planning organising self created':2,'works well with routine':3},
    'Decisions':{'indecisive changes mind easily':1,'rapid decision making sees things clearly':2,'slow to decide commits once chosen Prefers to follow a plan':3},
    'Thinking':{'creative thinker can get many ideas':1,'organised thinker entrepreneurial':2,'prefers to follow plan':3},
    'Projects':{'many at once, often does not finish':1,'organised and logical goal focused':2,'resists change likes simplicity':3},
    'Financial':{'spends impusively':1,'spends on luxuries spends on achieving purpose':2,'wealthy good money preserver':3},
    'physical activity':{'hyperactive lots of movement':1,'purposeful for reason':2,'slow calm':3},
    'sexual desire':{'strong desires fantasy but low energy':1,'moderate desire passionate dominating':2,'consistent desire loving nurturing':3}}

class Prakriti_Chatbot:
    def scroll_to_bottom(self):
        self.chat_history.yview_moveto(1.0)
    def __init__(self, root):
        self.root = root
        root.title("Prakriti Chatbot")
        self.spell_checker = SpellChecker() 
        self.chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.chat_history.grid(column=0, row=0, padx=10, pady=10, columnspan=3)

        self.user_input_entry = tk.Entry(root, width=40)
        self.user_input_entry.grid(column=0, row=1, padx=10, pady=10)

        self.send_button = tk.Button(root, text="Proceed", command=self.process_user_input)
        self.send_button.grid(column=1, row=1, padx=10, pady=10)

        self.greet_inputs = ['hello', 'hi', 'sup', 'hey']
        self.greet_responses = ['hi', 'hey!!', 'hi there', 'hello', 'I am glad! You are talking to me']

        self.chat_history.insert(tk.END, "Chatbot: Hello there! I am a chatbot here to talk about Prakriti body types...\n")
        self.chat_history.insert(tk.END, "Chatbot: To get started, I'll ask you some questions about your body and mind... Type start to continue...\n")
    def process_user_input(self):
        user_input = self.user_input_entry.get().lower()
        self.user_input_entry.delete(0, tk.END)

        if user_input in self.greet_inputs:
            response = random.choice(self.greet_responses)
            self.chat_history.insert(tk.END, f'User: {user_input}\n')
            self.chat_history.insert(tk.END, f'Chatbot: {response}\n')
        elif user_input=='start':
            response = self.evaluate_input()

    def evaluate_input(self):
        type1 = type2 = type3 = 0
        
        for y in [body_feature_mappings, intents_mind]:
            for feature, feature_values in y.items():
                x=0
                while x==0:
                    a = {}
                    print(f'Chatbot: Tell your {feature}')
                    for value in feature_values:
                        self.chat_history.insert(tk.END, f'BOT: {feature_values[value]}  {value}\n')
                        a[value] = feature_values[value]
                    self.scroll_to_bottom()
                    user_input=simpledialog.askstring("Input", f"Tell your {feature}:")
                             # Spell check and correction
                    self.chat_history.insert(tk.END, f'User: {user_input}\n')
                    r_input=''
                    print(user_input)
                    if user_input.isdigit():
                        if int(user_input)==1:
                            type1+=1;x=1
                        elif int(user_input)==2:
                            type2+=1;x=1
                        elif int(user_input)==3:
                            type3+=1;x=1
                    elif a:
                        for word in user_input.split():
                            corrected_word = self.spell_checker.correction(word)
                            r_input += corrected_word + " "
                        for value, score in a.items():
                            d = e = c = 0

                            for z in r_input.split():
                                
                                z=z.lower()
                                if z in value.lower():
                                    p = score
                                    print(score)
                                    if p == 1:
                                        d += 1
                                    elif p == 2:
                                        e += 1
                                    elif p == 3:
                                        c += 1

                            if d > e and d > c:
                                type1 += 1
                                x = 1
                                print('add')
                            elif e > d and e > c:
                                type2 += 1
                                x = 1
                                print('add2')
                            elif c > d and c > e:
                                type3 += 1
                                x = 1
                                print('add3')
                    
                    self.chat_history.insert(tk.END, f'BOT: {type1, type2, type3}\n')
                    self.chat_history.insert(tk.END,'-' * 40)
                    if x==0:
                        self.chat_history.insert(tk.END,'BOT: your input does not match please try again\n')
        self.scroll_to_bottom()        
        self.chat_history.insert(tk.END, f'BOT: {type1, type2, type3}\n')
        m = np.max([type1, type2, type3])
        if m == type1:
            category_input = 'vata'
            self.chat_history.insert(tk.END,'Chatbot: YOUR BODYTYPE IS VATA \n')
            print('Chatbot: YOUR BODYTYPE IS VATA')
        elif m == type2:
            category_input = 'pitta'
            self.chat_history.insert(tk.END,'Chatbot: YOUR BODYTYPE IS PITTA\n')
            print('Chatbot: YOUR BODYTYPE IS PITTA')
        elif m == type3:
            category_input = 'kapha'
            self.chat_history.insert(tk.END,'Chatbot: YOUR BODYTYPE IS KAPHA\n')
            print('Chatbot: YOUR BODYTYPE IS KAPHA')
        print('-' * 100)
        food_preferences = {
            'vata': {
                'general': ['food in small quantities', 'ginger', 'garlic'],
                'cereals': ['wheat', 'sesame'],
                'pulses': ['black gram', 'green gram'],
                'milk products': ['curd', 'ghee', 'butter', 'cheese'],
                'oils': ['sesame oil', 'castor oil', 'cod liver oil'],
                'vegetables': ['white gourd', 'drumstick', 'onion', 'asparagus', 'radish'],
                'fruits': ['mango', 'coconut', 'grapes', 'dates', 'pineapple', 'almonds', 'figs']
            },
            'pitta': {
                'general': ['cold', 'dry', 'sweet', 'bitter'],
                'cereals': ['wheat', 'barley'],
                'pulses': ['masur', 'greengram', 'channa'],
                'veggies': ['snake gourd', 'white gourd', 'carrot', 'beetroot'],
                'fruit': ['dried grapes', 'apple', 'pomegranate', 'ripe bananas'],
                'spices': ['coriander', 'rock salt'],
                'meat': ['deer', 'goat']
            },
            'kapha': {
                'general': ['light', 'hot', 'dry', 'pungent'],
                'cereals': ['barley'],
                'pulses': ['masur', 'horse gram', 'green gram'],
                'oils': ['mustard oil', 'sesame oil'],
                'veggies': ['bitter gourd', 'drumstick', 'snake gourd', 'onions'],
                'fruit': ['pomegranates', 'lemon'],
                'spices': ['dry ginger', 'black cumin seeds', 'garlic', 'pepper'],
                'other': ['old wine', 'honey']
            }
        }
        ''''''
        print('-'*100)
        print('FOOD PREFERENCES FOR ', category_input.upper())
        print('-'*100)
        #self.chat_history.insert(tk.END,)
        def print_food_preferences(category):
            if category in food_preferences:
                for group, items in food_preferences[category].items():
                    if group == 'general':
                        self.chat_history.insert(tk.END,'General:'+', '.join(items)+'\n')
                        print('General:'+ ', '.join(items))
                    else:
                        self.chat_history.insert(tk.END,f'{group.capitalize()}:'+', '.join(items)+'\n')
                        print(f'{group.capitalize()}:', ', '.join(items))
            else:
                print(f'Category "{category}" not found in food preferences.')
                self.chat_history.insert(tk.END,f'Category "{category}" not found in food preferences.')
                                         
        print_food_preferences(category_input)
        print('-'*100, '\n')
        self.chat_history.insert(tk.END,'-' * 40)
        life_style = {
            'communication': {'talkative': 'vata', 'sharp': 'pitta', 'incisive': 'pitta', 'communication with analytical abilities': 'pitta', 'less vocal': 'kapha', 'with good communication skills': 'kapha'},
            'Memory': {'quick': 'vata', 'grasping but poor retention': 'vata', 'Moderate': 'pitta', 'Grasping retention': 'pitta', 'slow': 'kapha', 'grasping but good retention': 'kapha'},
            'Initiation_Capabilities': {'quick': 'vata', 'responsive': 'vata', 'moderate': 'pitta', 'understanding': 'pitta', 'slow': 'kapha'},
            'Emotional_Temperature': {'fearful': 'vata', 'moody': 'vata', 'unpredictable': 'vata', 'aggressive': 'pitta', 'jealous': 'pitta', 'impatience': 'pitta', 'calm': 'kapha', 'attached': 'kapha', 'likeable': 'kapha'},
            'Pulse': {'thready': 'vata', 'feeble': 'vata', 'moves like a snake': 'vata', 'moderate': 'pitta', 'jumping like a frog': 'pitta', 'slow': 'kapha', 'moves like a swan': 'kapha'}
#the idea save all recieved inputs in a list if anything gone wrong recurse it and apply saved 
        }
        print('-'*100)
        print('LIFESTYLE PREFERENCES FOR ', category_input.upper())
        print('-'*100)
        def print_keys_and_values_by_value(value):
            found = False
            for key, val_dict in life_style.items():
                if value in val_dict.values():
                    found = True
                    matching_keys = [k for k, v in val_dict.items() if v == value]
                    for matching_key in matching_keys:
                        self.chat_history.insert(tk.END,f"Bot:  {key}-{matching_key}\n")
                        print(f"{key}-{matching_key}")
            if not found:
                print(f'No keys found with value {value}.')
        print_keys_and_values_by_value(category_input)
        print('-'*100)
        self.chat_history.insert(tk.END,'-' * 40)
        return[type1,type2,type3]

if __name__ == "__main__":
    root = tk.Tk()
    chatbot = Prakriti_Chatbot(root)
    root.mainloop()'''