############
Introduction
############

What is this about?
===================

A guide for ML projects with an emphasis on practices, workflows and tools to go from problem to solution.

guide - a patterns-based approach to broadly apply ML to diverse problems/domains
practices - an agile, test-driven development mindset that favors small steps, lazy development, fast iterations, working backwards, focussing on the product/consumer/user always.
workflows - automate the boring stuff
tools - an opinionated set of tools for the task. The right tool makes all the difference.

Having worked on the various stages of the ML development lifecycle I would often ponder about the big picture - the common patterns that persist across problems and what can be learned from them.
My research on end-to-end ML led to many wonderful resources.

While there are several great resources out there, I felt they are quite fragmented, which is fine, except it can be quite challenging to piece together a reliable solution, every time you apply ML to a new problem.
There are also several complete resources aka full-stack resources. These are great, however, the order of how things are presented or the ordering of priority is questionable.

I remember feeling overwhelmed by the steps, tools, grunt work, etc.
My goal is to not overwhelm but to craftfully navigage the terrain that is changing ever so quickly.

It's easy to see why it can be overwhelming or hard to bind everything together cause of the plethhora of topics/subjects that are being straddle under the umbrella of a ML project or production grade ML.
Software development - programming, testing and debugging
Software engineering - project scaffolding, version control, CI/CD, docs, automation
Data science - data, viz.
ML/DL - frameworks and libraries
Theory - Linear algebra, Statistics, Theory of Random Numbers, Optimization,

This will be a series of posts that are hands-on.

I start with a rather simple problem (simple only due to the advent of deep learning and what it has accomplished) and demonstrate the various stages of the deMLopment process, one step at a time.
It has the unrealistic expectation of being broad and deep (get it?) ;)

what is deMLopment?
===================

a play on words - putting ML in development (of the software kind) :)

Why?
====

There are several great resources out there for literally anything you want to do, so why this?

#. Problem understanding with an emphasis on data, fesability and how the result will be consumed.


#. Building the inference endpoint - a test-driven and agile state of mind

   - Start with a minimal set of tools and install tools as needed - Python via pyenv, PDM, VS Code, Pytest
   - Aim for functionality, not perfection. Hack it till you make it!
   - Spaghetti code away! Don't worry about project scaffolding, just yet.
   - Do care about good coding practices, for instance, keep all the constants separate so they can be moved to an external config. file.
   - Red-Blue-Refactor
   - Treat as development (editable) module.
   - Add existing model from model zoo.
   - Test a single image - take care to `unsqueeze` the image tensor.

   **Consuming the inference endpoint - IPYNB, CLI, web resource(URI) - local; cloud/remote**



#. Brief interlude

   - project scaffolding, code formatting and styling, version control, unifying steps with make, Docker for reproducibility and portability.


#. Serving and Monitoring

   Framework for serving, metrics for monitoring - system, model, data.


#. Model Testing and Deployment

   Testing includes load (endpoint) testing, A/B testing, etc. Strategies for deployment and triggers for retraining.


#. Model (re)Training


#. Data Management
