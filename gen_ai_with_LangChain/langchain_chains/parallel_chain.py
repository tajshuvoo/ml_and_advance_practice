from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

load_dotenv()

llm1 = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation"
)

model1 = ChatHuggingFace(llm=llm1)


llm2 = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text-generation"
)

model2 = ChatHuggingFace(llm=llm2)

prompt1 = PromptTemplate(
    template='Generate short and simple notes from the following text \n {text}',
    input_variables=['text']
)

prompt2 = PromptTemplate(
    template='Generate 5 short question and answer from the following text \n {text}',
    input_variables=['text']
)

prompt3 = PromptTemplate(
    template='Merge the provided notes and quiz into a single document \n notes -> {notes} \n quiz -> {quiz}',
    input_variables=['notes','quiz']
)

parser = StrOutputParser()

parallel_chain = RunnableParallel({
    'notes': prompt1 | model1 | parser,
    'quiz' : prompt2 | model2 | parser
})

merge_chain = prompt3 | model1 | parser

chain = parallel_chain | merge_chain

text= """
Support Vector Machine (SVM) Algorithm
Last Updated : 13 Nov, 2025
Support Vector Machine (SVM) is a supervised machine learning algorithm used for classification and regression tasks. It tries to find the best boundary known as hyperplane that separates different classes in the data. It is useful when you want to do binary classification like spam vs. not spam or cat vs. dog.

what_is_svm_.webpwhat_is_svm_.webp
The main goal of SVM is to maximize the margin between the two classes. The larger the margin the better the model performs on new and unseen data.

Key Concepts of Support Vector Machine
Hyperplane: A decision boundary separating different classes in feature space and is represented by the equation wx + b = 0 in linear classification.
Support Vectors: The closest data points to the hyperplane, crucial for determining the hyperplane and margin in SVM.
Margin: The distance between the hyperplane and the support vectors. SVM aims to maximize this margin for better classification performance.
Kernel: A function that maps data to a higher-dimensional space enabling SVM to handle non-linearly separable data.
Hard Margin: A maximum-margin hyperplane that perfectly separates the data without misclassifications.
Soft Margin: Allows some misclassifications by introducing slack variables, balancing margin maximization and misclassification penalties when data is not perfectly separable.
C: A regularization term balancing margin maximization and misclassification penalties. A higher C value forces stricter penalty for misclassifications.
Hinge Loss: A loss function penalizing misclassified points or margin violations and is combined with regularization in SVM.
Dual Problem: Involves solving for Lagrange multipliers associated with support vectors, facilitating the kernel trick and efficient computation.
How does Support Vector Machine Algorithm Work?
The key idea behind the SVM algorithm is to find the hyperplane that best separates two classes by maximizing the margin between them. This margin is the distance from the hyperplane to the nearest data points (support vectors) on each side.

SVM
Multiple hyperplanes separate the data from two classes
The best hyperplane also known as the "hard margin" is the one that maximizes the distance between the hyperplane and the nearest data points from both classes. This ensures a clear separation between the classes. So from the above figure, we choose L2 as hard margin. Let's consider a scenario like shown below:

2
Selecting hyperplane for data with outlier
Here, we have one blue ball in the boundary of the red ball.

How does SVM classify the data?
The blue ball in the boundary of red ones is an outlier of blue balls. The SVM algorithm has the characteristics to ignore the outlier and finds the best hyperplane that maximizes the margin. SVM is robust to outliers.

3
Hyperplane which is the most optimized one
A soft margin allows for some misclassifications or violations of the margin to improve generalization. The SVM optimizes the following equation to balance margin maximization and penalty minimization:

Objective Function
=
(
1
margin
)
+
λ
∑
penalty 
Objective Function=( 
margin
1
​
 )+λ∑penalty 

The penalty used for violations is often hinge loss which has the following behavior:

If a data point is correctly classified and within the margin there is no penalty (loss = 0).
If a point is incorrectly classified or violates the margin the hinge loss increases proportionally to the distance of the violation.
Till now we were talking about linearly separable data that seprates group of blue balls and red balls by a straight line/linear line.

What if data is not linearly separable?
When data is not linearly separable i.e it can't be divided by a straight line, SVM uses a technique called kernels to map the data into a higher-dimensional space where it becomes separable. This transformation helps SVM find a decision boundary even for non-linear data.

4
Original 1D dataset for classification
A kernel is a function that maps data points into a higher-dimensional space without explicitly computing the coordinates in that space. This allows SVM to work efficiently with non-linear data by implicitly performing the mapping. For example consider data points that are not linearly separable. By applying a kernel function SVM transforms the data points into a higher-dimensional space where they become linearly separable.

Linear Kernel: For linear separability.
Polynomial Kernel: Maps data into a polynomial space.
Radial Basis Function (RBF) Kernel: Transforms data into a space based on distances between data points.
5
Mapping 1D data to 2D to become able to separate the two classes
In this case the new variable y is created as a function of distance from the origin.

Mathematical Computation of SVM
Consider a binary classification problem with two classes, labeled as +1 and -1. We have a training dataset consisting of input feature vectors X and their corresponding class labels Y. The equation for the linear hyperplane can be written as:

w
T
x
+
b
=
0
w 
T
 x+b=0

Where:

w
w is the normal vector to the hyperplane (the direction perpendicular to it).
b
b is the offset or bias term representing the distance of the hyperplane from the origin along the normal vector 
w
w.
Distance from a Data Point to the Hyperplane
The distance between a data point 
x
i
x 
i
​
 and the decision boundary can be calculated as:

d
i
=
w
T
x
i
+
b
∣
∣
w
∣
∣
d 
i
​
 = 
∣∣w∣∣
w 
T
 x 
i
​
 +b
​
 

where ||w|| represents the Euclidean norm of the weight vector w.

Linear SVM Classifier
Distance from a Data Point to the Hyperplane:

y
^
=
{
1
:
 
w
T
x
+
b
≥
0
−
1
:
  
w
T
x
+
b
 
<
0
y
^
​
 ={ 
1
−1
​
  
: w 
T
 x+b≥0
:  w 
T
 x+b <0
​
 

Where 
y
^
y
^
​
  is the predicted label of a data point.

Optimization Problem for SVM
For a linearly separable dataset the goal is to find the hyperplane that maximizes the margin between the two classes while ensuring that all data points are correctly classified. This leads to the following optimization problem:

minimize
w
,
b
1
2
∥
w
∥
2
w,b
minimize
​
  
2
1
​
 ∥w∥ 
2
 

Subject to the constraint:

y
i
(
w
T
x
i
+
b
)
≥
1
f
o
r
i
=
1
,
2
,
3
,
⋯
,
m
y 
i
​
 (w 
T
 x 
i
​
 +b)≥1fori=1,2,3,⋯,m

Where:

y
i
y 
i
​
 ​ is the class label (+1 or -1) for each training instance.
x
i
x 
i
​
 ​ is the feature vector for the 
i
i-th training instance.
m
m is the total number of training instances.
The condition 
y
i
(
w
T
x
i
+
b
)
≥
1
y 
i
​
 (w 
T
 x 
i
​
 +b)≥1 ensures that each data point is correctly classified and lies outside the margin.

Soft Margin in Linear SVM Classifier
In the presence of outliers or non-separable data the SVM allows some misclassification by introducing slack variables 
ζ
i
ζ 
i
​
 ​. The optimization problem is modified as:

minimize 
w
,
b
1
2
∥
w
∥
2
+
C
∑
i
=
1
m
ζ
i
w,b
minimize 
​
  
2
1
​
 ∥w∥ 
2
 +C∑ 
i=1
m
​
 ζ 
i
​
 

Subject to the constraints:

y
i
(
w
T
x
i
+
b
)
≥
1
−
ζ
i
and
ζ
i
≥
0
for 
i
=
1
,
2
,
…
,
m
y 
i
​
 (w 
T
 x 
i
​
 +b)≥1−ζ 
i
​
 andζ 
i
​
 ≥0for i=1,2,…,m

Where:

C
C is a regularization parameter that controls the trade-off between margin maximization and penalty for misclassifications.
ζ
i
ζ 
i
​
 ​ are slack variables that represent the degree of violation of the margin by each data point.
Dual Problem for SVM
The dual problem involves maximizing the Lagrange multipliers associated with the support vectors. This transformation allows solving the SVM optimization using kernel functions for non-linear classification.

The dual objective function is given by:

maximize 
α
1
2
∑
i
=
1
m
∑
j
=
1
m
α
i
α
j
t
i
t
j
K
(
x
i
,
x
j
)
−
∑
i
=
1
m
α
i
α
maximize 
​
  
2
1
​
 ∑ 
i=1
m
​
 ∑ 
j=1
m
​
 α 
i
​
 α 
j
​
 t 
i
​
 t 
j
​
 K(x 
i
​
 ,x 
j
​
 )−∑ 
i=1
m
​
 α 
i
​
 

Where:

α
i
α 
i
​
 ​ are the Lagrange multipliers associated with the 
i
t
h
i 
th
  training sample.
t
i
t 
i
​
 ​ is the class label for the 
i
t
h
i 
th
 -th training sample.
K
(
x
i
,
x
j
)
K(x 
i
​
 ,x 
j
​
 ) is the kernel function that computes the similarity between data points 
x
i
x 
i
​
 ​ and 
x
j
x 
j
​
 ​. The kernel allows SVM to handle non-linear classification problems by mapping data into a higher-dimensional space.
The dual formulation optimizes the Lagrange multipliers 
α
i
α 
i
​
 ​ and the support vectors are those training samples where 
α
i
>
0
α 
i
​
 >0.

SVM Decision Boundary
Once the dual problem is solved, the decision boundary is given by:

w
=
∑
i
=
1
m
α
i
t
i
K
(
x
i
,
x
)
+
b
w=∑ 
i=1
m
​
 α 
i
​
 t 
i
​
 K(x 
i
​
 ,x)+b

Where 
w
w is the weight vector, 
x
x is the test data point and 
b
b is the bias term. Finally the bias term 
b
b is determined by the support vectors, which satisfy:

t
i
(
w
T
x
i
−
b
)
=
1
⇒
b
=
w
T
x
i
−
t
i
t 
i
​
 (w 
T
 x 
i
​
 −b)=1⇒b=w 
T
 x 
i
​
 −t 
i
​
 

Where 
x
i
x 
i
​
 ​ is any support vector.

This completes the mathematical framework of the Support Vector Machine algorithm which allows for both linear and non-linear classification using the dual problem and kernel trick.

Types of Support Vector Machine
Based on the nature of the decision boundary, Support Vector Machines (SVM) can be divided into two main parts:

Linear SVM: Linear SVMs use a linear decision boundary to separate the data points of different classes. When the data can be precisely linearly separated, linear SVMs are very suitable. This means that a single straight line (in 2D) or a hyperplane (in higher dimensions) can entirely divide the data points into their respective classes. A hyperplane that maximizes the margin between the classes is the decision boundary.
Non-Linear SVM: Non-Linear SVM can be used to classify data when it cannot be separated into two classes by a straight line (in the case of 2D). By using kernel functions, nonlinear SVMs can handle nonlinearly separable data. The original input data is transformed by these kernel functions into a higher-dimensional feature space where the data points can be linearly separated. A linear SVM is used to locate a nonlinear decision boundary in this modified space. 
Implementing SVM Algorithm Using Scikit-Learn
We will predict whether cancer is Benign or Malignant using historical data about patients diagnosed with cancer. This data includes independent attributes such as tumor size, texture, and others. To perform this classification, we will use an SVM (Support Vector Machine) classifier to differentiate between benign and malignant cases effectively.

load_breast_cancer(): Loads the breast cancer dataset (features and target labels).
SVC(kernel="linear", C=1): Creates a Support Vector Classifier with a linear kernel and regularization parameter C=1.
svm.fit(X, y): Trains the SVM model on the feature matrix X and target labels y.
DecisionBoundaryDisplay.from_estimator(): Visualizes the decision boundary of the trained model with a specified color map.
plt.scatter(): Creates a scatter plot of the data points, colored by their labels.
plt.show(): Displays the plot to the screen.

"""
result = chain.invoke({'text':text})

print(result)