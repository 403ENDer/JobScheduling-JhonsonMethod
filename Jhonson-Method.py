import streamlit as st
import numpy as np
import pandas as pd


job_list = []
def make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        st.header(f'Job {i+1}')
        with st.container():
            grid[i] = st.columns(rows,gap="medium")
    return grid

def johnson_method(jobs):
        machine_1 = []
        machine_2 = []

        for job in jobs:
            if job[0] < job[1]:
                machine_1.append(job)
            else:
                machine_2.append(job)

        machine_1.sort(key=lambda x: x[0])
        machine_2.sort(key=lambda x: x[1], reverse=True)

        schedule = machine_1 + machine_2
        return schedule

def calculate(machine_mat ,  rows, cols):
        jobs = int(rows)
        machines = int(cols)

        machine_1 = np.zeros((jobs, 2))
        if machines > 2:
            for i in range(len(machine_mat)):
                machine_1[i, 0] = machine_mat[i, 0] + machine_mat[i,1]
                machine_1[i, 1] = sum([x for x in machine_mat[i]]) - machine_mat[i, 0]
        else:
            machine_1 = machine_mat

        schedule = johnson_method(machine_1.tolist())

        job_list = []
        for i in schedule:
            job_list.append(machine_1.tolist().index(i) + 1)
        return schedule  , job_list 
def starting_ending(time , job_list):
        machine = np.zeros((len(time), 4))

        k = 0
        for i in range(len(time)):
            machine[i, 0] = k
            machine[i, 1] = k = k + time[i][0]

        y = 0
        for i in range(len(time)):
            if i != 0:
                k = machine[i, 1]
                if k > y:
                    machine[i, 2] = k
                    machine[i, 3] = y = k + time[i][1]
                else:
                    machine[i, 2] = y
                    machine[i, 3] = y = y + time[i][1]
            else:
                machine[i, 2] = machine[i, 1]
                machine[i, 3] = y = machine[i, 2] + time[i][1]

        df = pd.DataFrame(
            machine,
            columns=["Starting time 1", "Ending Time 1", "Starting time 2", "Ending time 2"],
            index=job_list
        )
        df.insert(0, 'Job', job_list)

        # Ideal Time of machine 2
        ideal = [df["Starting time 2"][job_list[0]]]
        for i in range(1, len(job_list)):
            ideal.append(df["Starting time 2"][job_list[i]] - df["Ending time 2"][job_list[i - 1]])
        df["Ideal time of Machine 2"] = ideal
        return df


def display_schedule(df):
        df1 = df
        st.dataframe(df1)
        print(df, df['Ending time 2'].iloc[-1])
        ideal_a = df["Ending time 2"].iloc[-1] - df["Ending Time 1"].iloc[-1]
        ideal_b = int(sum(df["Ideal time of Machine 2"]))
        total = df["Ending time 2"].iloc[-1]

        st.write("Ideal time of A:", ideal_a)
        st.write("Ideal time of B:", ideal_b)
        st.write("Total completion time:", total)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap');

html, body, [class*="css"] {
    font-weight: 500;
}
</style>""",
unsafe_allow_html=True)



hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;} 
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

#st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.header('Jhonson Method of Job scheduling')
st.markdown("""---""")

col1,col2=st.columns(2)

with col1:
    rows = st.number_input('Enter number of Jobs:' ,  value=0)
with col2:
    cols = st.number_input('Enter number of Machine:' , value= 0)

st.button('Generate:checkered_flag:')



try:
    if (rows==0 and cols==0):
        st.write("Enter Machine and Jobs to create a matrix.")
    elif (rows==0):
        st.write("Enter Machine to create a matrix.")
    elif (cols==0):
        st.write("Enter Jobs to create a matrix.")
    else:
        mygrid = make_grid(rows,cols)
except:
  pass

l=[]
l1=[]
for i in range(rows):
    for j in range(cols):
        a=mygrid[i][j].number_input(":",key=(i*10+j),label_visibility="collapsed",value=0,step=0)
        l.append(a)
    l1.append(l)   
    l=[]

print(l1)
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)

st.markdown(
    """
<style>
body{
    text-align:center;
    background-color:#0f4c81;
}
div.stButton > button:first-child { 
height: 3em;
width: 42em; 
}</style>
""",
    unsafe_allow_html=True,
)
st.markdown(
    """
    <style>
    body {
        background-color: white;  
    }
    </style>
    """,
    unsafe_allow_html=True
)

submit=st.button("Submit")

al=[]
if submit:
    try:
        schedule , job_lis = calculate(np.array(l1) , rows , cols)
        st.write( "Optimal order of Jobs :", "->".join((map(str , job_lis))))
        df = starting_ending(schedule , job_lis)
        display_schedule(pd.DataFrame(df))
    except:
        pass


    

