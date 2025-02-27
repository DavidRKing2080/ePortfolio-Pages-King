---
title: David King's ePortfolio
---

##CS 499 Computer Science Capstone

I'm currently testing the homepage feature by writing a faux description. Please ignore blah blah.

## Professional Self-Assessment

<p style="text-indent: 55px;">
My coding experience began in high school, with enlistment into the software engineering branch of the STEM program. There I learned the basics of java via the eclipse IDE and worked on projects centered around application and game design. I maintained a personal hobby of game modding until and after pursuing my associates of Computer Science at Tidewater Community College. While at TCC I was able to learn a variety of additional languages such as C++ and Python. In addition to this, my work as an office specialist at Chesapeake’s Department of Human Services had me redesigning their website via WordPress. This included teaching myself how to manipulate HTML elements and create new ones based on limited knowledge of the language. During this time, I also finished a career study certificate in cyber security.
</p>

<p style="text-indent: 55px;">
The Southern New Hampshire University degree program refined and expanded my skillset to include knowledge of database management systems such as MySQL, as well as advanced coding concepts like dynamic testing through Maven. I also learned about office-side workflow methodologies such as agile and turning stakeholder requests into coded features. One course included methods for building and training path-finding AI to demonstrate how machine learning can be applied to applications. An emphasis of most of the coding classes was security, through means such as testing and industry-standard practices like input validation and dependency review.
</p>

<p style="text-indent: 55px;">
My ePortfolio includes three artifacts that demonstrate improvement in the categories of software design, data structures, and databases. The first is a buffer overflow checker that has been improved with a wider range of checks, more robust error handling, and clearer error messaging. The second artifact is a hash table that was recoded with improved collision handling and dynamic resizing. Finally the third artifact was a database manager that was improved with indexing and input validation, as well as restructured to lend modularity.
</p>

## CS 499 Course Outcomes

Through my code review and follow-up enhancements, I strove to meet the following outcomes for the course:

-Employ strategies for building collaborative environments that enable diverse audiences to support organizational decision making in the field of computer science
-Design, develop, and deliver professional-quality oral, written, and visual communications that are coherent, technically sound, and appropriately adapted to specific audiences and contexts
-Design and evaluate computing solutions that solve a given problem using algorithmic principles and computer science practices and standards appropriate to its solution, while managing the trade-offs involved in design choices
-Demonstrate an ability to use well-founded and innovative techniques, skills, and tools in computing practices for the purpose of implementing computer solutions that deliver value and accomplish industry-specific goals
-Develop a security mindset that anticipates adversarial exploits in software architecture and designs to expose potential vulnerabilities, mitigate design flaws, and ensure privacy and enhanced security of data and resources

## Code Review

Text for formatting.

## Artifact 1: Software Engineering and Design

<p style="text-indent: 55px;">
The enhanced artifact is a buffer overflow checker that was created back in Module One of CS 405 (Secure Coding). Its functionality includes checking for overflow and underflow using a list of common variable types.
</p>

<p style="text-indent: 55px;">  
While simple in function, the artifact represents a good early project with the potential to be rewritten in a way that follows best practices such as input validation, clear error messaging, good comments, and solid test coverage. In this way, simplicity serves to highlight how my skills have grown by providing a basic template of comparison. The artifact itself has been improved via the addition of modular helper functions, more explicit error handling, expanded data type coverage, and edge case handling.
</p>
  
<p style="text-indent: 55px;">  
My intended course outcome with these changes was the development of a security mindset. I believe that I’ve satisfied the outcome by writing in robust error handling and expanding test coverage.
</p>

<p style="text-indent: 55px;">
During the process of enhancement, I was able to see the effectiveness of modularization. Separating reusable logic into helper functions leaves the code easier to maintain and reduces redundancy. The addition of multiple data types and extreme values also ensured that the program functioned correctly under different conditions. There were some limitations that came with difficulty, such as triggering certain errors without getting silent. These were overcome with structured error handling and more detailed exceptions.
</p>

## Artifact 2: Algorithms and Data Structures

<p style="text-indent: 55px;">
The enhanced artifact is a hash table implementation originally written for CS 300 (Structures and Algorithms, Analysis and Design). It makes use of a hash table and CSV parser to efficiently retrieve, read, parse, store, and display bid data from a CSV sheet.
</p>

<p style="text-indent: 55px;">
The hash table was effective at dealing with a limited data set but used chaining for collision resolution and could not be resized dynamically. This would naturally result in performance issues in instances of a growing data set. I enhanced the artifact by improving collusion handling using open addressing with linear probing, rather than chaining. This reduces memory fragmentation and improvement performance. I also implemented dynamic resizing and optimized the hash function itself via multiplicative string hashing. These changes cut down significantly on the number of lines in the artifact, as the program now requires fewer pointers and no recursive node traversal.
</p>

<p style="text-indent: 55px;">
Three course outcomes were focused on for this implementation. Those were efficient data structure utilization, algorithmic thinking, and code maintainability and scalability. Efficient data structure utilization was met by implementing optimized hashing and dynamic resizing. Algorithmic thinking was covered via a transition to open addressing and multiplicative hashing. Finally, code maintainability and scalability were satisfied through a new modular implementation that will make future modifications easier.
</p>

<p style="text-indent: 55px;">
Linear probing has an issue with excessive clustering, so implementation required testing to determine when resizing should occur. Attention was paid to performance, to decide which hashing strategy was best optimized for the showcased artifact. A major lesson learned was the effectiveness of refactoring. The new implementation uses far fewer lines of code and overall represents a better implementation for the artifact’s intended functionality.
</p>

## Artifact 3: Databases

<p style="text-indent: 55px;">
The enhanced artifact is a database manager for an animal shelter. It was written as the final project for CS 340 (Advanced Programming Concepts). The manager uses MongoDB to manage CRUD operations for the shelter’s database. These operations are standard for databases and include storage, retrieval, updating, and deletion.
</p>

<p style="text-indent: 55px;">
The manager was selected because it showcases my ability to create and optimize database-driven applications. While the original artifact did its job well, there was room for improvement. Data validation was added to the create function to avoid invalid record insertion. This lends extra security to the application. An optimization function was added to create indexes on frequently queried fields, which lends more efficiency to the manager. The code was also refactored to increase modularity, allowing for future scalability.
</p>

<p style="text-indent: 55px;">
Originally, only two course outcomes were intended for this implementation, those being design and evaluate computing solutions and develop a security mindset. Implementing indexing and input validation displays how algorithmic problem-solving can be balanced with performance. The input validation also prevents bad or incomplete data from being inserted, reducing vulnerabilities and lends credence towards a secure mindset. However, the enhancement did also cover the additional outcome of building a collaborative environment. The optimization of queries enables better data retrieval and decision-making, which supports collaborative operations in the animal shelter.
</p>

<p style="text-indent: 55px;">
Originally, the plan was to add an advanced search function to the artifact. However, this would have required tampering with more than a single artifact. Given that the objective is to show straightforward enhancements to artifact functionality, this change was decided against. Moreover, fully refactoring the code required testing different versions for implementation and selecting the best one. Overall, the final artifact is more stable, secure, and efficient than now when compared to where it was in the beginning of the process. It will serve as a good display of my ability to engage in backend development, especially in regard to databases.
</p>
