import collections
import pandas as pd
import random
import yaml

def show_TOC():             #print table of contents
    with open('recipe.yaml','r') as file:
        data = yaml.safe_load(file)
        toc_list = []
        for m in data.keys():
            toc_list.append(m)
        return sorted(toc_list)

def print_recipe(r,data):   #print formatted recipe
    cook_list=[]
    for i,j in data[r]['ingredient'].items():
        for k,q in data[r]['ingredient'][i].items():
            cook_list.append((q,k,i))
    return (r,sorted(cook_list),data[r]['instructions'])
                
def show_Cookbook():        #print cookbook
    with open('recipe.yaml','r') as file:
        data = yaml.safe_load(file)
        cook = []
        for key, value in data.items():
            cook.append(print_recipe(key,data))
        return sorted(cook)

def random_recipe():        #print x number of random recipes    
    with open('recipe.yaml','r') as file:
        data = yaml.safe_load(file)        
        random_list = random.sample(data.keys(),int(1))
        rando_lst = []
        for r in random_list:
            y = print_recipe(r,data)
        return (y)     
  
def recipe_search(search_text): #print a single recipe by name
    with open('recipe.yaml','r') as file:
        data = yaml.safe_load(file)
        if search_text in data:            
            print_recipe(search_text,data)
            return (print_recipe(search_text,data))

def set_DOWMeal_Random(): #set random dinner for M,W,F
    with open('weeklymealplan.yaml','r') as planfile:        
        dow_dict = yaml.safe_load(planfile)
    dow, meal = random.choice(list(dow_dict.items()))

    with open('recipe.yaml','r') as file:
            data = yaml.safe_load(file)
            random_list = random.sample(data.keys(),int(3))
            meal = dow_dict['Monday']['Dinner'] = random_list[0]
            meal2 = dow_dict['Wednesday']['Dinner'] = random_list[1]
            meal3 = dow_dict['Friday']['Dinner'] = random_list[2]            
            
    with open('weeklymealplan.yaml','w') as file:
        dump = yaml.dump(dow_dict,file,default_flow_style = False)
        
def change_plan(day_to_change,meal_to_change,rec_to_add):  #add recipe
    with open('weeklymealplan.yaml','r') as planfile:        
        dow_dict = yaml.safe_load(planfile)
        dow_dict[day_to_change][meal_to_change] = rec_to_add
        with open('weeklymealplan.yaml','w') as changefile:
            dump = yaml.dump(dow_dict,changefile,default_flow_style = False)
  
def clear_DOWMeal_ALL(): #clear meal plan
    with open('weeklymealplan.yaml','w') as file:
        dow_dict = {'Monday':{'Breakfast':'',
                              'Lunch':'',
                              'Dinner':''},
                    'Tuesday':{'Breakfast':'',
                              'Lunch':'',
                              'Dinner':''},
                    'Wednesday':{'Breakfast':'',
                              'Lunch':'',
                              'Dinner':''},
                    'Thursday':{'Breakfast':'',
                              'Lunch':'',
                              'Dinner':''},                    
                    'Friday':{'Breakfast':'',
                              'Lunch':'',
                              'Dinner':''},
                    'Saturday':{'Breakfast':'',
                              'Lunch':'',
                              'Dinner':''},
                    'Sunday':{'Breakfast':'',
                              'Lunch':'',
                              'Dinner':''},}        

        dump = yaml.dump(dow_dict,file,default_flow_style = False)
        
def grocery_list(): #create a list of ingredients based on meal plan
    groc_rec = []
    groc_list = []
    with open('weeklymealplan.yaml','r') as file:
        data = yaml.safe_load(file)
        for i,k in data['Monday'].items():
            groc_rec.append(k)
        for i,k in data['Tuesday'].items():
            groc_rec.append(k)
        for i,k in data['Wednesday'].items():
            groc_rec.append(k)
        for i,k in data['Thursday'].items():
            groc_rec.append(k)
        for i,k in data['Friday'].items():
            groc_rec.append(k)
        for i,k in data['Saturday'].items():
            groc_rec.append(k)
        for i,k in data['Sunday'].items():
            groc_rec.append(k)
    groc_rec = [i for i in groc_rec if i]

    with open('recipe.yaml','r') as file:
        data = yaml.safe_load(file)
        for r in groc_rec:            
            for i,j in data[r]['ingredient'].items():
                for k,q in data[r]['ingredient'][i].items():                    
                    groc_list.append((i,q,k))
    groc_list = pd.DataFrame(groc_list).groupby([0,2])[1].sum().reset_index().to_numpy()
    groc_list = [tuple(p) for p in groc_list]

    with open('weeklygrocerylist.txt','w') as grocfile:
        grocfile.write('Recipe Summary: \n')
        for i in groc_rec:
            grocfile.write('-' +str(i) + '\n')       
        grocfile.write('\nIngredient List: \n')
        for p in sorted(groc_list):            
            grocfile.write('-' + str(p[0])+ ', ' + str(p[2]) + ' ' +str(p[1]) + '\n')
    return [groc_list]
        
def add_recipe(recipe_name,ingredients_lst,instructions_full):    #insert new recipe in cookbook
    add_rec_dict = {recipe_name:{'ingredient':ingredients_lst,'instructions':instructions_full}}

    with open('recipe.yaml','a') as file:
        dump = yaml.safe_dump(add_rec_dict,file,sort_keys=False,default_flow_style=0,default_style='|')

