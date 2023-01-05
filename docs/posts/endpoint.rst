#############################
Create the Inference Endpoint
#############################

        I tried so hard and got so far
        In the end it doesn't even matter...
        - Linkin Park

Why Start at the End?
=====================

Lets start at the end...

Build a Prediction API
======================

There are two approaches here.

1. a `predict` function that takes in an image and returns the predicted class. This approach is perfectly valid for this instance. This also lends itself nicely to a serverless deployment strategy.
2. a `WrittenTextRecognizer` class that exposes a `predict` method. This allows for encapsulating other methods and provides a way for interacting with a prediction object rather than a single fixed function.

What should the prediction API do?

provide a class for creating prediction objects
expose a method for making predictions
load the saved model for making inference
transform the input image to match the model input requirement
run the transformed input through the model
convert the model predicted output into a format consumable by upstream processes
provide a command-line interface for getting predictions
support single file and batch mode operations
package the prediction class as a module for importing into other modules

How should we proceed? A benefit of using a test-driven development approach is it puts you in control of the pace and manage complexity, fear, etc.

We will write small tests and just enough code to pass the tests and iterate over this process many times, pausing on occassion for reviewing and refactoring, as necessary.


