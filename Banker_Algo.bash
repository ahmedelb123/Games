#!/bin/bash

# Banker's Algorithm Implementation
# This script implements the Banker's Algorithm for deadlock avoidance in operating systems
# The algorithm determines if resource allocation to processes is in a safe state
# It also optimizes process execution order using Shortest Process Next (SPN) scheduling

# In this program:
# - Columns represent different Resource types (R0, R1, R2, etc.)
# - Rows represent different Processes (P0, P1, P2, etc.)

# Function to ensure valid input for number of processes
getNumberOfProcesses() {
	while true;do
		read -p "Enter the number of processes: " processes
		if [[ $processes =~ ^[0-9]+$ ]];then
			 echo $processes
            		return 
		else
			printf "This input is invalid. Please enter a positive  number!\n" >&2
		fi
	done
}

# Function to ensure valid input for number of resource types
getNumberOfResource() {
    while true;do
            read -p "Enter the number of resources: " resources
            if [[ $resources =~ ^[0-9]+$ ]];then
                 echo $resources
                return
            else
                printf "This input is invalid. Please enter a positive number:\n" >&2 
            fi
    done
}

# Helper function to compute the sum of elements in an array
# Used for resource availability calculations
giveSumOfArr() {
    arr=("$@")
    sum=0

    for num in "${arr[@]}"; do
        sum=$((sum + num))
    done

    echo $sum
}

# Function to collect execution time for each process
# This is used for process scheduling optimization later
getExecutionTimeOfEachProcesse() {
    rows=$1
    ExecutionTimeOfEachProcesse=()
    printf "Please Enter the time needed of each process to be executed:\n" >&2
    for((i = 0; i<rows; i++));do
        while true;do
        read -p "Enter time needed for P$i: " value
        if ! [[ $value =~ ^[0-9]+$ ]];then
                printf "This input is invalid. Please enter a positive number!\n" >&2
        else
                ExecutionTimeOfEachProcesse[$i]=$value
                break
        fi
        done
    done
    echo ${ExecutionTimeOfEachProcesse[@]}
}

# Implementation of Shortest Process Next (SPN) algorithm
# This optimizes the execution sequence by ordering processes based on their execution time
# Shorter execution time processes get priority to improve overall system performance
SPNAlgo() {
    executionTime=("$@")
    # Sort execution times in ascending order
    sortedExecutionTime=($(echo "${executionTime[@]}" | tr ' ' '\n' | sort -n))
    alreadyExistProcessIndex=()
    optimizedSafeDomain=()

    # Create a new execution sequence based on execution time
    for num in "${sortedExecutionTime[@]}";do
        for i in "${!executionTime[@]}"; do
             if [[ "${executionTime[i]}" == "$num" && ! " ${alreadyExistProcessIndex[@]} " =~ " $i " ]]; then
                    optimizedSafeDomain+=("$i")
                    alreadyExistProcessIndex+=("$i")
                    break
	     fi
        done
    done
    echo ${optimizedSafeDomain[@]}
}

# Calculate the average turnaround time for process execution
# Used to evaluate scheduling efficiency before and after optimization
giveAverageTime() {
    executionTime=("$@")
    length=${#executionTime[@]}
    averageTime=0
    cumulativeSum=0 

    # Calculate waiting time for each process in sequence
    for num in "${executionTime[@]}";do
        averageTime=$((averageTime + cumulativeSum))
        cumulativeSum=$((cumulativeSum + num))
    done
    # Calculate average waiting time
    averageTime=$(echo "scale=2; $averageTime / $length" | bc)
    echo $averageTime
}

# Function to collect available instances of each resource type
# These are resources not yet allocated to any process
getAvailableResources() {
    cols=$1
    availableResources=()
    printf "Please Enter the resources of each resource instance:\n" >&2
    for((i = 0; i<cols; i++));do
        while true;do
            read -p "Enter availability for R$i: " value
            if ! [[ $value =~ ^[0-9]+$ ]];then
                printf "This input is invalid. Please enter a positive number!\n" >&2
            else
                availableResources[$i]=$value
                break
            fi
        done
    done
    echo ${availableResources[@]}
}

# Function to collect maximum resource needs for each process
# This is the maximum number of each resource type a process might need
getMaxResources() {
    cols=$1
    rows=$2
    maxMatrix=()
    printf "Please Enter the maximum demand of each process:\n" >&2
    for((i = 0; i < rows;i++));do
        for((j =0 ; j<cols; j++));do
            while true;do
                read -p "Enter max value of R$j of P$i: " value
                if ! [[ $value =~ ^[0-9]+$ ]];then
                      printf "This input is invalid. Please enter a positive number!\n" >&2
                else
                    maxMatrix[$((i * cols + j))]=$value     
                    break
                fi
            done
        done
    done
    echo ${maxMatrix[@]}
}

# Function to collect currently allocated resources for each process
# These are resources already assigned to each process
getAllocatedResources() {
    cols=$1
    rows=$2
    maxMatrix=("${@:3}")
    allocatedMatrix=()
    printf "Please Enter the allocated resources of each process:\n" >&2
    for((i = 0; i < rows;i++));do
        for((j = 0 ; j < cols; j++));do
                while true;do
                     read -p "Enter allocated value of R$j of P$i: " value
                     if ! [[ $value =~ ^[0-9]+$ ]];then
                          printf "This input is invalid. Please enter a positive number!\n" >&2
                      # Validation: allocated resources cannot exceed max declared needs
                      elif [[ ${maxMatrix[$((i * cols + j))]} -lt $value ]];then 
                         printf "This value is bigger than the max of the process resource give another value which is less than the max!\n" >&2
                     else
                        allocatedMatrix[$((i * cols + j))]=$value
                        break
                     fi
                done
        done
    done
    echo ${allocatedMatrix[@]}
}

# Calculate the Need matrix which is Max - Allocated
# This represents additional resources each process might request
computeNeeds() {
    cols=$1
    rows=$2
    shift 2  # Shift past first two arguments
    allocatedMatrix=("${@:1:cols*rows}") # Extract allocatedMatrix from arguments
    maxMatrix=("${@:cols*rows+1}") # Extract maxMatrix

    needMatrix=()
    for ((i = 0; i < rows; i++)); do
        for ((j = 0; j < cols; j++)); do
            index=$((i * cols + j))
            needMatrix[$index]=$((maxMatrix[$index] - allocatedMatrix[$index]))
        done
    done

    echo ${needMatrix[@]}
}

# Update the available resources when a process completes
# Adds the allocated resources back to available pool
giveNewWork() {
    cols=$1
    work=("${@:1:cols}")       # Available resources
    allocation=("${@:cols + 1}")  # Resources to be released back to system
    newWork=()

    for ((i = 0; i < 3; i++)); do
        newWork[$i]=$((work[$i] + allocation[$i]))
    done

    echo ${newWork[@]}
}

# Utility function to print matrices in a formatted way
printMatrix() {
    cols=$1
    rows=$2
    shift 2  # Remove the first two arguments
    matrix=("$@")

    echo -n "   "  # Space for row labels

    for ((j = 0; j < cols; j++)); do
        echo -n "R$j "
    done
    echo

    for ((i = 0; i < rows; i++)); do
        echo -n "P$i "  
        for ((j = 0; j < cols; j++)); do
            index=$((i * cols + j))
            printf "%-3s" "${matrix[index]}"
        done
        echo
    done
}

# Print Need matrix with execution times
printNeedMatrix() {
    cols=$1
    rows=$2
    shift 2  # Remove the first two arguments

    # Extract the execution times from the last 'rows' arguments
    exec_times=("${@:1:rows}")
    matrix=("${@:rows + 1}")

    echo -n "   "  # Space for row labels

    for ((j = 0; j < cols; j++)); do
        echo -n "R$j "
    done
    echo "Time"  # Add a column for execution time

    for ((i = 0; i < rows; i++)); do
        echo -n "P$((i)) "  
        for ((j = 0; j < cols; j++)); do
            index=$((i * cols + j))
            printf "%-3s" "${matrix[index]}"
        done
        echo "${exec_times[i]}"  # Print the execution time
    done
} 

# Function to get user input for adding new processes
addNewProcesse() {
    while true;do
        read -p "Do you want to add process (Y|N): " answer
        ans=${answer^^}

        if [[ "$ans" == "Y" || "$ans" == "N" ]];then
            echo "$ans";
            return
        else
            printf "Please enter Y for Yes and N for No!\n" >&2
        fi
    done
}

# Helper function to update matrix by appending new resources
updateMatrix() {
    cols=$1
    shift 1
    newResources=("$@") 
    shift $cols
    newMatrix=("$@") 
    for ((i = 0; i < cols; i++)); do
        newMatrix+=(${newResources[$i]})
    done
    echo ${newMatrix[@]}
}

# Get execution time for newly added process
getExecutionTimeOfNewPRocess() {
    rows=$1
    shift 1
    newExecutionTimeList=("$@")
    while true;do
        read -p "Enter the time execution of the new process P$rows: " value
        if ! [[ $value =~ ^[0-9]+$ ]];then
                printf "This input is invalid. Please enter a positive number!\n" >&2
        else
                newExecutionTimeList+=($value)
                break
        fi
    done
    echo ${newExecutionTimeList[@]}
}

# Get max resource needs for a newly added process
maxResourceOfNewProcess() {
    cols=$1
    rows=$2
    shift 2
    newMaxMatrix=("$@")

    printf "Please Enter the max resources of this new process:\n" >&2
    for((i = 0; i<cols; i++));do
        while true;do
		read -p "Enter max resource of P$((rows - 1)) for R$i: " value
            if ! [[ $value =~ ^[0-9]+$ ]];then
                printf "This input is invalid. Please enter a positive number!\n" >&2
            else
                newMaxMatrix+=($value)
                break
            fi
        done
    done
    echo ${newMaxMatrix[@]}
}

# Display the safe execution sequence of processes
printSafeSequence() {
    safeDomain=("$@")
    echo "Safe Domain"
    echo 
    for i in "${safeDomain[@]}";do
        printf "P$i -> "
    done
    printf "\n\n"
}

# Display available resources information
printAvailableResources() {
    cols=$1
    shift 1
    arr=("$@")
    echo
    
    for (( i = 0; i < cols; i++ ));do
        printf "R$i "
    done
    echo

    for j in "${arr[@]}";do
        printf "$j  "
    done
    printf "\n\n"
}

# Main function implementing the Banker's Algorithm
# This determines if the system is in a safe state and finds a safe execution sequence
computeSafeSequence() {
    safeDomain=()  # Holds processes that can execute safely
    unsafeDomain=() # Holds processes that might cause deadlock
    cols=$(getNumberOfResource)  # Number of resource types
    rows=$(getNumberOfProcesses)   # Number of processes
    numberOfUnexecutedProcesses=$rows
    
    # Get information about available resources
    availableMatrix=($(getAvailableResources "$cols"))
    # This one dont change so when the user add a new process the availabilty will change to origine 
    origineAvailbality=("${availableMatrix[@]}")
    printAvailableResources $cols ${availableMatrix[@]}
    
    # Get execution times for performance optimization
    executionTimeOfEachProcess=($(getExecutionTimeOfEachProcesse "$rows"))
    averageTime=($(giveAverageTime "${executionTimeOfEachProcess[@]}"))
       
    # Collect the maximum resource needs for each process
    maxMatrix=($(getMaxResources "$cols" "$rows"))
    echo -e "\n"
    echo "Max Matrix" 
    printMatrix "$cols" "$rows" "${maxMatrix[@]}"
    echo -e "\n"  
    
    # Collect currently allocated resources for each process
    allocatedMatrix=($(getAllocatedResources "$cols" "$rows" "${maxMatrix[@]}"))
    echo -e "\n"
    echo "Allocated Matrix"  
    printMatrix "$cols" "$rows" "${allocatedMatrix[@]}"
    echo -e "\n"    
    
    # Calculate additional resources each process might need (Need = Max - Allocated)
    needMatrix=($(computeNeeds "$cols" "$rows" "${allocatedMatrix[@]}" "${maxMatrix[@]}"))
    echo -e "\n"
    echo "Need Matrix"
    printNeedMatrix "$cols" "$rows" "${executionTimeOfEachProcess[@]}" "${needMatrix[@]}"
    echo -e "\n"
    
    # Main Banker's Algorithm loop: finds a safe execution sequence if one exists
    while true; do
        numberOfExecutedProcesses=0
        
        # Check each process to see if it can be safely executed
        for ((i = 0; i < rows; i++)); do
            # Skip processes already in the safe domain
            if [[ " ${safeDomain[*]} " =~ " $i " ]]; then
                continue
            fi

            # Flag to check if all resource needs can be satisfied
            canExecute=true
            allocatedResourcesForProcesse=()
            
            # Check each resource type individually
            for ((j = 0; j < cols; j++)); do
                needValue=${needMatrix[$((i * cols + j))]}
                availableValue=${availableMatrix[$j]}
                
                # If any resource need exceeds available, process cannot execute
                if (( needValue > availableValue )); then
                    canExecute=false
                    break
                fi
                
                # Store allocated resources for this process to release later
                allocatedResourcesForProcesse+=(${allocatedMatrix[$((i * cols + j))]})
            done
            
            # If all resource needs can be satisfied, add process to safe domain
            if $canExecute; then
                safeDomain+=("$i")
                numberOfExecutedProcesses=$((numberOfExecutedProcesses + 1))
                numberOfUnexecutedProcesses=$((numberOfUnexecutedProcesses - 1))
                # Add released resources back to available pool
                availableMatrix=($(giveNewWork "${availableMatrix[@]}" "${allocatedResourcesForProcesse[@]}"))
            else
                unsafeDomain+=("$i")
            fi
        done

        # Check if system is in deadlock (no process can be safely executed)
        if (( numberOfExecutedProcesses == 0 && numberOfUnexecutedProcesses > 0 )); then
            echo "This system is not safe"
            return
        # All processes can be executed safely
        elif (( numberOfUnexecutedProcesses == 0 )); then
            echo "This system is safe"
            echo
            printSafeSequence ${safeDomain[@]}
            echo "The Average time Of the safe sequence is: $averageTime s"
            echo
            sortedExecutionTime=($(echo "${executionTimeOfEachProcess[@]}" | tr ' ' '\n' | sort -n))

            # Optimize the execution sequence using Shortest Process Next algorithm
            optimazedSafeDomain=($(SPNAlgo "${executionTimeOfEachProcess[@]}"))
            optimizedAverageTime=($(giveAverageTime "${sortedExecutionTime[@]}"))
            echo "The safe sequence after the SPN algorithm."
            echo
            printSafeSequence ${optimazedSafeDomain[@]}
            echo "The new  Average time Of the safe sequence is after SPN algorithm is : $optimizedAverageTime s"
            echo

            # Check if user wants to add a new process and repeat the algorithm
            newProcesse=$(addNewProcesse)
            if [[ "$newProcesse" == "Y" ]]; then
                rows=$((rows + 1))
    
                maxMatrix=($(maxResourceOfNewProcess "$cols" "$rows" "${maxMatrix[@]}"))
                newProcessMaxResources=("${maxMatrix[@]:$((${#maxMatrix[@]} - cols))}")
    
                allocatedMatrix=($(updateMatrix "$cols" "${newProcessMaxResources[@]}" "${allocatedMatrix[@]}"))
                needMatrix=($(updateMatrix "$cols" "${newProcessMaxResources[@]}" "${needMatrix[@]}"))
		availableMatrix=("${origineAvailbality[@]}")

                numberOfUnexecutedProcesses=$rows
                executionTimeOfEachProcess=($(getExecutionTimeOfNewPRocess "$rows" "${executionTimeOfEachProcess[@]}"))
                safeDomain=()
                unsafeDomain=()
            else
                echo "End of program"
                return
            fi
        fi
    done
}
computeSafeSequence

