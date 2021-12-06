# ThumbGAN


This repository will record progress and final result of my subbmission for the course project in Applied Deep learning.


### Project Summary

**Relevant Literature:**

Here listed you will find the three most relevant papers this project will draw from:

The first one by Reed et al. discribes a similar method, creating images from text, but in the context of image creation from visual descriptions.

The second one is a heavily cited paper introducing the technique of a skip-gram model for word embedding. I plan to use this method or one based on it to generate the word vectors used as input in conjunction with the pictures.

Third is a paper by Goodfellow et al. which is heavily cited as the basis for the concept of Generative Adversarial Networks as a whole.

[1] Reed, S., Akata, Z., Yan, X., Logeswaran, L., Schiele, B. &amp; Lee, H.. (2016). Generative Adversarial Text to Image Synthesis. <i>Proceedings of The 33rd International Conference on Machine Learning</i>, in <i>Proceedings of Machine Learning Research</i> 48:1060-1069 Available from https://proceedings.mlr.press/v48/reed16.html.

[2] Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2013). Efficient estimation of word representations in vector space. arXiv preprint arXiv:1301.3781.

[3] Goodfellow, I., Pouget-Abadie, J., Mirza, M., Xu, B., Warde-Farley, D., Ozair, S., ... & Bengio, Y. (2014). Generative adversarial nets. Advances in neural information processing systems, 27.


For PDF versions of the relevant papers and other ones that fit the topic please have a look at the Literature folder.

**Choice of Topic:** 
Generating Video Thumbnails from Video Title Text and assigned Tags using a Generative Adversarial Network

**Project Type:** Bring your own Data, Bring our own Method

**Project Description:**

The main goal for this project is to create and train a network that can generate passable YouTube video thumbnails based on a title and a set of tags. The network in question shall be structured similarly to what is described in Reed et al. (2016), Generative Adversarial Text to Image Synthesis. 

Their method proposes training of a Generative Adversarial Network (GAN) to synthesize pictures based on vector embeddings of a sentence describing the picture contents. I want to follow this approach regarding the network structure, but use a different method to generate the word embeddings for its input. In the past I achieved good results using pre-trained word vectors, provided for example as part of the fastText library, as input for neural networks. This seems to me to be a logical decision as it reduces the scale of the project in an aspect that is not its primary scope.

A data set will be created in which real video thumbnails are combined with their title and tags as found on YouTube.com. This will be done making use of the API provided by YouTube itself. Due to the large diversity on YouTube a sub selection of search terms will be chosen to serve as a basis for data collection. This hopefully enables the network to find patterns more easily thereby keeping the size of the training set at a reasonable level. 

To set a reasonable goal and to quantify the concept of a "passable" image two thresholds are defined. The first is the percentage of percentage of images correctly classified as real by the dicriminator. The second is the percentage of pictures created bu the generator that could fool the discriminator. Each of these values alone does not identify a model as 'good', but in conjunction they create a quantifyable standard to work towards.


### Time Estimates

![plot](./Gantt.png)
