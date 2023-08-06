NAIT (Neural Artificial Intelligence Tool)

NAIT is module for super easily training and using neural networks.
Its developed so that people with little to no knowledge of neural networks can use it.


Usage
--------------------

    To train a network:

        Training model setup:

            To train a NAIT network you will need a set of two lists.
            The first list is the inputs, which will be of any number of values.
            The values MUST be float values so one input could be [1.0, 1.0, 1.0, 1.0]
            You dont need to have multiple inputs, but you need to put the inputs in a list. (exaple: [[1.0, 1.0, 1.0, 1.0]])
            To use multiple inputs you can simple put more inputs in that list. (exaple: [[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0]])
            You now need a set of what output you would want for each of those inputs.
            This list is formatted the same way as the inputs but can still have a different number of values. (exaple: [[10.0, 10.0], [20.0, 20.0]])
            The last step is to combine the inputs and expectations into a list so the final training model should look like this:
            [[
                [1.0, 1.0, 1.0, 1.0],
                [2.0, 2.0, 2.0, 2.0]
            ], [
                [10.0, 10.0],
                [20.0, 20.0]
            ]]

        Actual training:

            Before you train your network with your training model you will first need to choose the complexity of your network.
            There is three levels of complexity: simple, standard and complex
            The more complex your network is, the longer it takes to train and the worse it might be at more basic tasks.
            You also need to decide for how long you want to train it for.
            You define how long it trains for in epochs which is 3000 generations each.
            Now to start the training you use the function: nait.<complexity>.train(<training model>, <number of epochs>)
            You want to get the minimal loss and the maximum accuracy so if you are getting a high loss and low accuracy try some different settings.
            When the network is done training, it saves itself to 'nait_model.py', if there already is a 'nait_model.py' file, it overwrites it.
            You are now ready to use the network.

    To use a network:

        Setup:

            To use a network you first need a 'nait_model.py' file in the same directory.
            You now use the function nait.<complexity>.load(<inputs>)

        Inputs:
            
            You can input a pre-trained network a list of floats but the number of values must be the same as how the network was trained. (example: [1.0, 1.0, 1.0, 1.0])
            You can also give it multiple input lists at the same time. (example: [[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0]])
            It will then return a output of as many values as it was trained on. (example: [[10.0, 10.0], [20.0, 20.0]])