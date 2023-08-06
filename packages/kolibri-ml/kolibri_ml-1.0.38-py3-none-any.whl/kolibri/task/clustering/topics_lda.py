#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import logging
import os
import random
import tempfile
from kolibri.data import resources
from pathlib import Path
from kolibri.indexers import TextIndexer
from kolibri.task.clustering.baseTopic import TopicModel
import pandas as pd
import numpy as np


logger = logging.getLogger(__name__)

TOPIC_MODEL_FILE_NAME = "topic_model.pkl"


class TopicModel(TopicModel):
    """Python wrapper for LDA using `MALLET <http://mallet.cs.umass.edu/>`_.

    Communication between MALLET and Python takes place by passing around data files on disk
    and calling Java with subprocess.call().

    Warnings
    --------
    This is **only** python wrapper for `MALLET LDA <http://mallet.cs.umass.edu/>`_,
    you need to install original implementation first and pass the path to binary to ``mallet_path``.

    """


    provides = ["topics"]

    requires = ["tokens"]

    defaults = {
        "fixed": {
            "nb_topic_start": 1,
            "nb_topic_stop": 1,
            "step": 1,
            "workers": 4,
            "embeddings_dim": 50,
            "random_seed": 0,
            "output_folder": ".",
            "model": "lda",
            "algorithm": "gibbs"
        },
        "tunable": {
            "num_topics": 20,

            # The maximum number of iterations for optimization algorithms.
            "alpha": 50,
            "optimize_interval": 0,
            "iterations": 200,
            "topic_threshold": 0.0,
            "use_lemma": True,
        }
    }

    def __init__(self, component_config=None, prefix=None):

        super().__init__(component_config=component_config)
        self.start = self.get_parameter("nb_topic_start")
        self.stop = self.get_parameter("nb_topic_stop")
        self.step=self.get_parameter("step")

        self.indexer=TextIndexer()
        if self.start > self.stop:
            raise Exception("In topic experimentation start should be larger than stop.")
        self.model=None
        if self.get_parameter("algorithm")=="gibbs":
            self.mallet_path = resources.get(str(Path('modules', 'clustering', 'mallet'))).path
            self.mallet_path = os.path.join(self.mallet_path, 'bin/mallet')
        self.model_type=self.get_parameter("model", "lda")
        self.algorithm=self.get_parameter("algorithm", "gibbs")

        self.num_topics = self.get_parameter("num_topics")
        self.topic_threshold = self.get_parameter("topic_threshold")
        self.alpha = self.get_parameter("alpha")
        if prefix is None:
            rand_prefix = hex(random.randint(0, 0xffffff))[2:] + '_'
            prefix = os.path.join(tempfile.gettempdir(), rand_prefix)
        self.prefix = prefix
        self.workers = self.get_parameter("workers")
        self.optimize_interval = self.get_parameter("optimize_interval")
        self.iterations = self.get_parameter("iterations")
        self.random_seed = self.get_parameter("random_seed")
        self.topic_model = None

    def fit(self, X, y, X_val=None, y_val=None, **kwargs):
        """Train Mallet LDA.
        Parameters
        ----------
        corpus : iterable of iterable of (int, int)
            Corpus in BoW format
        """


        self.indexer.build_vocab(X, None)

        self.num_terms =len(self.indexer.vocab2idx)
        corpus = [self.indexer.doc2bow(doc) for doc in X]
        """

        This function trains a given topic model_type.
        Returns:
            Trained Model

        """

        multi_core=(self.get_parameter("n_jobs")==-1 or self.get_parameter("n_jobs")>1)
        import sys

        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        if logger.hasHandlers():
            logger.handlers.clear()

        ch = logging.FileHandler("logs.log")
        ch.setLevel(logging.DEBUG)


        logger.info("Initializing create_model()")
        logger.info(
            """create_model(model_type=lda, multi_core={}, num_topics={})""".format(
                 str(self.get_parameter("n_jobs")==-1), str(self.num_topics)
            )
        )

        logger.info("Checking exceptions")

        # run_time
        import datetime, time

        runtime_start = time.time()

        # ignore warnings
        import warnings

        warnings.filterwarnings("ignore")

        # checking for allowed algorithms
        allowed_models = ["lda", "lsi", "hdp", "rp", "nmf"]

        if self.model_type not in allowed_models:
            sys.exit(
                "(Value Error): Model Not Available. Please see docstring for list of available models."
            )

        if self.num_topics is not None:
            if self.num_topics <= 1:
                sys.exit("(Type Error): num_topics parameter only accepts integer value.")


        # pre-load libraries
        import numpy as np
        import ipywidgets as ipw
        from IPython.display import display, clear_output, update_display
        import datetime, time

        """
        monitor starts
        """

        logger.info("Preparing display monitor")

        progress = ipw.IntProgress(
            value=0, min=0, max=4, step=1, description="Processing: "
        )


        display(progress)


        progress.value += 1

        """
        monitor starts
        """

        logger.info("Defining topic model_type")

        # define topic_model_name
        if self.model_type == "lda":
            topic_model_name = "Latent Dirichlet Allocation"
        elif self.model_type == "lsi":
            topic_model_name = "Latent Semantic Indexing"
        elif self.model_type == "hdp":
            topic_model_name = "Hierarchical Dirichlet Process"
        elif self.model_type == "nmf":
            topic_model_name = "Non-Negative Matrix Factorization"
        elif self.model_type == "rp":
            topic_model_name = "Random Projections"

        logger.info("Model: " + str(topic_model_name))


        logger.info("num_topics set to: " + str(self.num_topics))

        progress.value += 1

        model_fit_start = time.time()

        if self.model_type == "nmf":

            from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
            from sklearn.decomposition import NMF
            from sklearn.preprocessing import normalize

            logger.info(
                "CountVectorizer, TfidfTransformer, NMF, normalize imported successfully"
            )

            text_join = []

            for i in X:
                word = " ".join(i)
                text_join.append(word)

            progress.value += 1

            vectorizer = CountVectorizer(analyzer="word", max_features=5000)
            x_counts = vectorizer.fit_transform(text_join)
            logger.info("CountVectorizer() Fit Successfully")
            transformer = TfidfTransformer(smooth_idf=False)
            x_tfidf = transformer.fit_transform(x_counts)
            logger.info("TfidfTransformer() Fit Successfully")
            xtfidf_norm = normalize(x_tfidf, norm="l1", axis=1)
            self.model = NMF(n_components=self.num_topics, init="nndsvd", random_state=self.get_parameter("seed"), **kwargs)
            self.model.fit(xtfidf_norm)
            logger.info("NMF() Trained Successfully")

        elif self.model_type == "lda":

            if multi_core:
                logger.info("LDA multi_core enabled")
                if self.algorithm=="variational":
                    from gensim.models.ldamulticore import LdaMulticore

                    logger.info("LdaMulticore imported successfully")

                    self.model = LdaMulticore(
                        corpus=corpus,
                        num_topics=self.num_topics,
                        id2word=self.indexer.idx2vocab,
                        workers=4,
                        random_state=self.get_parameter("seed"),
                        chunksize=100,
                        passes=10,
                        alpha="symmetric",
                        per_word_topics=True,
                        **kwargs
                    )

                    logger.info("LdaMulticore Variational model_type trained successfully")

                    progress.value += 1
                elif self.algorithm=="gibbs":
                    from kolibri.task.clustering.mallet import LdaMallet
                    self.model=LdaMallet(self.mallet_path,
                                                           corpus=corpus,
                                                           iterations=self.iterations,
                                                            num_topics=self.num_topics,
                                                            id2word=self.indexer.idx2vocab,
                                                           workers=4)

                    logger.info("LdaMulticore Gibbs model_type trained successfully")

                    progress.value += 1
            else:

                from gensim.models.ldamodel import LdaModel

                logger.info("LdaModel imported successfully")

                if self.get_parameter("algorithm")=="variational":

                    self.model = LdaModel(
                        corpus=corpus,
                        num_topics=self.num_topics,
                        id2word=self.indexer.idx2vocab,
                        random_state=self.get_parameter("seed"),
                        update_every=1,
                        chunksize=100,
                        passes=10,
                        alpha="auto",
                        per_word_topics=True,
                        **kwargs
                    )

                    logger.info("LdaModel trained successfully")

                    progress.value += 1

                elif self.get_parameter("algorithm") == "gibbs":
                    from kolibri.task.clustering.mallet import LdaMallet
                    self.model = LdaMallet(self.mallet_path,
                                                             corpus=corpus,
                                                             iterations=self.iterations,
                                                             num_topics=self.num_topics,
                                                             id2word=self.indexer.idx2vocab)

                    logger.info("LdaMulticore Gibbs model_type trained successfully")

                    progress.value += 1

        elif self.model_type == "lsi":

            from gensim.models.lsimodel import LsiModel

            logger.info("LsiModel imported successfully")

            self.model = LsiModel(corpus=corpus, num_topics=self.num_topics, id2word=self.indexer.idx2vocab, **kwargs)

            logger.info("LsiModel trained successfully")

            progress.value += 1

        elif self.model_type == "hdp":

            from gensim.models import HdpModel

            logger.info("HdpModel imported successfully")

            self.model = HdpModel(
                corpus=corpus,
                id2word=self.indexer.idx2vocab,
                random_state=self.get_parameter("seed"),
                chunksize=100,
                T=self.num_topics,
                **kwargs
            )

            logger.info("HdpModel trained successfully")

            progress.value += 1

        elif self.model_type == "rp":

            from gensim.models import RpModel

            logger.info("RpModel imported successfully")

            self.model = RpModel(corpus=corpus, id2word=self.indexer.idx2vocab, num_topics=self.num_topics, **kwargs)

            logger.info("RpModel trained successfully")

            progress.value += 1

        model_fit_end = time.time()
        model_fit_time = np.array(model_fit_end - model_fit_start).round(2)

        progress.value += 1

        # end runtime
        runtime_end = time.time()
        runtime = np.array(runtime_end - runtime_start).round(2)



        # storing into experiment
        clear_output()

        logger.info(str(self.model))
        logger.info(
            "fit() succesfully completed......................................"
        )


    def predict(self, X,  verbose=True):

        """
        This function assigns topic labels to the dataset for a given model_type.



        model_type: trained model_type object, default = None
            Trained model_type object


        verbose: bool, default = True
            Status update is not printed when verbose is set to False.


        Returns:
            pandas.DataFrame

        """

        if self.model_type == "lda":
            corpus = [self.indexer.doc2bow(doc) for doc in X]
            if self.algorithm=="variational":
                c = self.model.get_document_topics(corpus, minimum_probability=0)
            elif self.algorithm=="gibbs":
                c = self.model.get_document_topics(corpus)


            ls = []
            for i in range(len(c)):
                ls.append(c[i])
            bb = []
            for i in ls:
                bs = []
                for k in i:
                    bs.append(k[1])
                bb.append(bs)

            Dominant_Topic = []
            for i in bb:
                max_ = max(i)
                max_ = i.index(max_)
                Dominant_Topic.append("Topic " + str(max_))

            pdt = []
            for i in range(0, len(bb)):
                l = max(bb[i]) / sum(bb[i])
                pdt.append(round(l, 2))

            col_names = []
            for i in range(len(self.model.show_topics(num_topics=999999))):
                a = "Topic_" + str(i)
                col_names.append(a)


            bb_ = pd.DataFrame(bb, columns=col_names)
#            bb_ = pd.concat([data_, bb], axis=1)

            dt_ = pd.DataFrame(Dominant_Topic, columns=["Dominant_Topic"])
            bb_ = pd.concat([bb_, dt_], axis=1)

            pdt_ = pd.DataFrame(pdt, columns=["Perc_Dominant_Topic"])
            bb_ = pd.concat([bb_, pdt_], axis=1)


        elif self.model_type == "lsi":

            col_names = []
            for i in range(0, len(self.model.print_topics(num_topics=999999))):
                a = "Topic_" + str(i)
                col_names.append(a)

            df_ = pd.DataFrame()
            Dominant_Topic = []

            for i in range(0, len(X)):

                db = self.indexer.doc2bow(X[i])
                db_ = self.model[db]
                db_array = np.array(db_)
                db_array_ = db_array[:, 1]

                max_ = max(db_array_)
                max_ = list(db_array_).index(max_)
                Dominant_Topic.append("Topic " + str(max_))

                db_df_ = pd.DataFrame([db_array_])
                df_ = pd.concat([df_, db_df_])


            df_.columns = col_names

            df_["Dominant_Topic"] = Dominant_Topic
            df_ = df_.reset_index(drop=True)
 #           bb_ = pd.concat([data_, df_], axis=1)
            bb_=df_

        elif self.model_type == "hdp" or self.model_type == "rp":

            rate = []
            for i in range(0, len(X)):

                rate.append(self.model[X[i]])

            topic_num = []
            topic_weight = []
            doc_num = []
            counter = 0
            for i in rate:
                for k in i:
                    topic_num.append(k[0])
                    topic_weight.append(k[1])
                    doc_num.append(counter)
                counter += 1

            df = pd.DataFrame(
                {"Document": doc_num, "Topic": topic_num, "Topic Weight": topic_weight}
            ).sort_values(by="Topic")
            df = df.pivot(index="Document", columns="Topic", values="Topic Weight").fillna(
                0
            )
            df.columns = ["Topic_" + str(i) for i in df.columns]

            Dominant_Topic = []

            for i in range(0, len(df)):
                s = df.iloc[i].max()
                d = list(df.iloc[i]).index(s)
                v = df.columns[d]
                v = v.replace("_", " ")
                Dominant_Topic.append(v)

            df["Dominant_Topic"] = Dominant_Topic

#            bb_ = pd.concat([data_, df], axis=1)
            bb_=df
        elif self.model_type == "nmf":

            """
            this section will go away in future release through better handling
            """

            from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
            from sklearn.decomposition import NMF
            from sklearn.preprocessing import normalize

            text_join = []

            for i in X:
                word = " ".join(i)
                text_join.append(word)


            vectorizer = CountVectorizer(analyzer="word", max_features=5000)
            x_counts = vectorizer.fit_transform(text_join)
            transformer = TfidfTransformer(smooth_idf=False)
            x_tfidf = transformer.fit_transform(x_counts)
            xtfidf_norm = normalize(x_tfidf, norm="l1", axis=1)

            """
            section ends
            """

            bb = list(self.model.fit_transform(xtfidf_norm))

            col_names = []

            for i in range(len(bb[0])):
                a = "Topic_" + str(i)
                col_names.append(a)

            Dominant_Topic = []
            for i in bb:
                max_ = max(i)
                max_ = list(i).index(max_)
                Dominant_Topic.append("Topic " + str(max_))

            pdt = []
            for i in range(0, len(bb)):
                l = max(bb[i]) / sum(bb[i])
                pdt.append(round(l, 2))


            bb_ = pd.DataFrame(bb, columns=col_names)
#            bb_ = pd.concat([data_, bb], axis=1)

            dt_ = pd.DataFrame(Dominant_Topic, columns=["Dominant_Topic"])
            bb_ = pd.concat([bb_, dt_], axis=1)

            pdt_ = pd.DataFrame(pdt, columns=["Perc_Dominant_Topic"])
            bb_ = pd.concat([bb_, pdt_], axis=1)


        logger.info(str(bb_.shape))
        logger.info(
            "assign_model() succesfully completed......................................"
        )

        return bb_

    def plot(self, plot="frequency", topic_num=None, save=False, system=True, display_format=None):

        """
        This function takes a trained model_type object (optional) and returns a plot based
        on the inferred dataset by internally calling assign_model before generating a
        plot. Where a model_type parameter is not passed, a plot on the entire dataset will
        be returned instead of one at the topic level. As such, plot_model can be used
        with or without model_type. All plots with a model_type parameter passed as a trained
        model_type object will return a plot based on the first topic i.e.  'Topic 0'. This
        can be changed using the topic_num param.



        model_type: object, default = none
            Trained Model Object


        plot: str, default = 'frequency'
            List of available plots (ID - Name):

            * Word Token Frequency - 'frequency'
            * Word Distribution Plot - 'distribution'
            * Bigram Frequency Plot - 'bigram'
            * Trigram Frequency Plot - 'trigram'
            * Sentiment Polarity Plot - 'sentiment'
            * Part of Speech Frequency - 'pos'
            * t-SNE (3d) Dimension Plot - 'tsne'
            * Topic Model (pyLDAvis) - 'topic_model'
            * Topic Infer Distribution - 'topic_distribution'
            * Wordcloud - 'wordcloud'
            * UMAP Dimensionality Plot - 'umap'


        topic_num : str, default = None
            Topic number to be passed as a string. If set to None, default generation will
            be on 'Topic 0'


        save: string/bool, default = False
            Plot is saved as png file in local directory when save parameter set to True.
            Plot is saved as png file in the specified directory when the path to the directory is specified.


        system: bool, default = True
            Must remain True all times. Only to be changed by internal functions.


        display_format: str, default = None
            To display plots in Streamlit (https://www.streamlit.io/), set this to 'streamlit'.
            Currently, not all plots are supported.


        Returns:
            None


        Warnings
        --------
        -  'pos' and 'umap' plot not available at model_type level. Hence the model_type parameter is
           ignored. The result will always be based on the entire training corpus.

        -  'topic_model' plot is based on pyLDAVis implementation. Hence its not available
           for model_type = 'lsi', 'rp' and 'nmf'.
        """


        # setting default of topic_num
        if self.model is not None and self.topic_num is None:
            topic_num = "Topic 0"
            logger.info("Topic selected. topic_num : " + str(topic_num))

        import sys

        # plot checking
        allowed_plots = [
            "frequency",
            "distribution",
            "bigram",
            "trigram",
            "sentiment",
            "pos",
            "tsne",
            "topic_model",
            "topic_distribution",
            "wordcloud",
            "umap",
        ]
        if plot not in allowed_plots:
            sys.exit(
                "(Value Error): Plot Not Available. Please see docstring for list of available plots."
            )

        # handle topic_model plot error
        if plot == "topic_model":
            not_allowed_tm = ["lsi", "rp", "nmf"]
            if self.model_type in not_allowed_tm:
                sys.exit(
                    "(Type Error): Model not supported for plot = topic_model. Please see docstring for list of available models supported for topic_model."
                )

        # checking display_format parameter
        plot_formats = [None, "streamlit"]

        if display_format not in plot_formats:
            raise ValueError("display_format can only be None or 'streamlit'.")

        if display_format == "streamlit":
            try:
                import streamlit as st
            except ImportError:
                raise ImportError(
                    "It appears that streamlit is not installed. Do: pip install streamlit"
                )

        """
        error handling ends here
        """

        logger.info("Importing libraries")
        # import dependencies
        import pandas as pd
        import numpy

        # import cufflinks
        import cufflinks as cf

        cf.go_offline()
        cf.set_config_file(offline=False, world_readable=True)

        # save parameter

        if save:
            save_param = True
        else:
            save_param = False

        logger.info("save_param set to " + str(save_param))

        logger.info("plot type: " + str(plot))

        if plot == "frequency":

            try:

                from sklearn.feature_extraction.text import CountVectorizer

                def get_top_n_words(corpus, n=None):
                    vec = CountVectorizer()
                    logger.info("Fitting CountVectorizer()")
                    bag_of_words = vec.fit_transform(corpus)
                    sum_words = bag_of_words.sum(axis=0)
                    words_freq = [
                        (word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()
                    ]
                    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
                    return words_freq[:n]

                logger.info("Rendering Visual")

                if topic_num is None:
                    logger.warning("topic_num set to None. Plot generated at corpus level.")
                    common_words = get_top_n_words(data_[target_], n=100)
                    df2 = pd.DataFrame(common_words, columns=["Text", "count"])

                    if display_format == "streamlit":
                        df3 = (
                            df2.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title="Top 100 words after removing stop words",
                                asFigure=True  # plotly obj needs to be returned for streamlit to interpret
                            )
                        )

                        st.write(df3)

                    else:
                        df3 = (
                            df2.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title="Top 100 words after removing stop words",
                                asFigure=save_param,
                            )
                        )

                else:
                    title = (
                            str(topic_num) + ": " + "Top 100 words after removing stop words"
                    )
                    logger.info(
                        "SubProcess assign_model() called =================================="
                    )
                    assigned_df = assign_model(model, verbose=False)
                    logger.info(
                        "SubProcess assign_model() end =================================="
                    )
                    filtered_df = assigned_df.loc[
                        assigned_df["Dominant_Topic"] == topic_num
                        ]
                    common_words = get_top_n_words(filtered_df[target_], n=100)
                    df2 = pd.DataFrame(common_words, columns=["Text", "count"])

                    if display_format == "streamlit":
                        df3 = (
                            df2.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title=title,
                                asFigure=True  # plotly obj needs to be returned for streamlit to interpret
                            )
                        )

                        st.write(df3)

                    else:
                        df3 = (
                            df2.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title=title,
                                asFigure=save_param,
                            )
                        )

                logger.info("Visual Rendered Successfully")

                if save:
                    if not isinstance(save, bool):
                        plot_filename = os.path.join(save, "Word Frequency.html")
                    else:
                        plot_filename = "Word Frequency.html"
                    logger.info(f"Saving '{plot_filename}'")
                    df3.write_html(plot_filename)



            except:
                logger.warning(
                    "Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )
                sys.exit(
                    "(Value Error): Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )

        elif plot == "distribution":

            try:

                if topic_num is None:
                    logger.warning("topic_num set to None. Plot generated at corpus level.")
                    b = data_[target_].apply(lambda x: len(str(x).split()))
                    b = pd.DataFrame(b)
                    logger.info("Rendering Visual")

                    if display_format == "streamlit":
                        b = b[target_].iplot(
                            kind="hist",
                            bins=100,
                            xTitle="word count",
                            linecolor="black",
                            yTitle="count",
                            title="Word Count Distribution",
                            asFigure=True  # plotly obj needs to be returned for streamlit to interpret
                        )

                        st.write(b)

                    else:
                        b = b[target_].iplot(
                            kind="hist",
                            bins=100,
                            xTitle="word count",
                            linecolor="black",
                            yTitle="count",
                            title="Word Count Distribution",
                            asFigure=save_param
                        )

                else:
                    title = str(topic_num) + ": " + "Word Count Distribution"
                    logger.info(
                        "SubProcess assign_model() called =================================="
                    )
                    assigned_df = assign_model(model, verbose=False)
                    logger.info(
                        "SubProcess assign_model() end =================================="
                    )
                    filtered_df = assigned_df.loc[
                        assigned_df["Dominant_Topic"] == topic_num
                        ]

                    b = filtered_df[target_].apply(lambda x: len(str(x).split()))
                    b = pd.DataFrame(b)
                    logger.info("Rendering Visual")

                    if display_format == "streamlit":
                        b = b[target_].iplot(
                            kind="hist",
                            bins=100,
                            xTitle="word count",
                            linecolor="black",
                            yTitle="count",
                            title=title,
                            asFigure=True  # plotly obj needs to be returned for streamlit to interpret
                        )

                        st.write(b)

                    else:
                        b = b[target_].iplot(
                            kind="hist",
                            bins=100,
                            xTitle="word count",
                            linecolor="black",
                            yTitle="count",
                            title=title,
                            asFigure=save_param
                        )

                logger.info("Visual Rendered Successfully")

                if save:
                    if not isinstance(save, bool):
                        plot_filename = os.path.join(save, "Distribution.html")
                    else:
                        plot_filename = "Distribution.html"
                    logger.info(f"Saving '{plot_filename}'")
                    b.write_html(plot_filename)


            except:
                logger.warning(
                    "Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )
                sys.exit(
                    "(Value Error): Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )

        elif plot == "bigram":

            try:

                from sklearn.feature_extraction.text import CountVectorizer

                def get_top_n_bigram(corpus, n=None):
                    logger.info("Fitting CountVectorizer()")
                    vec = CountVectorizer(ngram_range=(2, 2)).fit(corpus)
                    bag_of_words = vec.transform(corpus)
                    sum_words = bag_of_words.sum(axis=0)
                    words_freq = [
                        (word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()
                    ]
                    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
                    return words_freq[:n]

                if topic_num is None:
                    logger.warning("topic_num set to None. Plot generated at corpus level.")
                    common_words = get_top_n_bigram(data_[target_], 100)
                    df3 = pd.DataFrame(common_words, columns=["Text", "count"])
                    logger.info("Rendering Visual")

                    if display_format == "streamlit":
                        df3 = (
                            df3.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title="Top 100 bigrams after removing stop words",
                                asFigure=True  # plotly obj needs to be returned for streamlit to interpret
                            )
                        )

                        st.write(df3)

                    else:
                        df3 = (
                            df3.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title="Top 100 bigrams after removing stop words",
                                asFigure=save_param
                            )
                        )

                else:
                    title = (
                            str(topic_num) + ": " + "Top 100 bigrams after removing stop words"
                    )
                    logger.info(
                        "SubProcess assign_model() called =================================="
                    )
                    assigned_df = assign_model(model, verbose=False)
                    logger.info(
                        "SubProcess assign_model() end =================================="
                    )
                    filtered_df = assigned_df.loc[
                        assigned_df["Dominant_Topic"] == topic_num
                        ]
                    common_words = get_top_n_bigram(filtered_df[target_], 100)
                    df3 = pd.DataFrame(common_words, columns=["Text", "count"])
                    logger.info("Rendering Visual")

                    if display_format == "streamlit":
                        df3 = (
                            df3.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title=title,
                                asFigure=True  # plotly obj needs to be returned for streamlit to interpret
                            )
                        )

                        st.write(df3)

                    else:
                        df3 = (
                            df3.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title=title,
                                asFigure=save_param
                            )
                        )

                logger.info("Visual Rendered Successfully")

                if save:
                    if not isinstance(save, bool):
                        plot_filename = os.path.join(save, "Bigram.html")
                    else:
                        plot_filename = "Bigram.html"
                    logger.info(f"Saving '{plot_filename}'")
                    df3.write_html(plot_filename)


            except:
                logger.warning(
                    "Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )
                sys.exit(
                    "(Value Error): Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )

        elif plot == "trigram":

            try:

                from sklearn.feature_extraction.text import CountVectorizer

                def get_top_n_trigram(corpus, n=None):
                    vec = CountVectorizer(ngram_range=(3, 3)).fit(corpus)
                    logger.info("Fitting CountVectorizer()")
                    bag_of_words = vec.transform(corpus)
                    sum_words = bag_of_words.sum(axis=0)
                    words_freq = [
                        (word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()
                    ]
                    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
                    return words_freq[:n]

                if topic_num is None:
                    logger.warning("topic_num set to None. Plot generated at corpus level.")
                    common_words = get_top_n_trigram(data_[target_], 100)
                    df3 = pd.DataFrame(common_words, columns=["Text", "count"])
                    logger.info("Rendering Visual")

                    if display_format == "streamlit":
                        df3 = (
                            df3.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title="Top 100 trigrams after removing stop words",
                                asFigure=True  # plotly obj needs to be returned for streamlit to interpret
                            )
                        )

                        st.write(df3)

                    else:
                        df3 = (
                            df3.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title="Top 100 trigrams after removing stop words",
                                asFigure=save_param
                            )
                        )

                else:
                    title = (
                            str(topic_num) + ": " + "Top 100 trigrams after removing stop words"
                    )
                    logger.info(
                        "SubProcess assign_model() called =================================="
                    )
                    assigned_df = assign_model(model, verbose=False)
                    logger.info(
                        "SubProcess assign_model() end =================================="
                    )
                    filtered_df = assigned_df.loc[
                        assigned_df["Dominant_Topic"] == topic_num
                        ]
                    common_words = get_top_n_trigram(filtered_df[target_], 100)
                    df3 = pd.DataFrame(common_words, columns=["Text", "count"])
                    logger.info("Rendering Visual")

                    if display_format == "streamlit":
                        df3 = (
                            df3.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title=title,
                                asFigure=True  # plotly obj needs to be returned for streamlit to interpret
                            )
                        )

                        st.write(df3)

                    else:
                        df3 = (
                            df3.groupby("Text")
                                .sum()["count"]
                                .sort_values(ascending=False)
                                .iplot(
                                kind="bar",
                                yTitle="Count",
                                linecolor="black",
                                title=title,
                                asFigure=save_param
                            )
                        )

                logger.info("Visual Rendered Successfully")

                if save:
                    if not isinstance(save, bool):
                        plot_filename = os.path.join(save, "Trigram.html")
                    else:
                        plot_filename = "Trigram.html"
                    logger.info(f"Saving '{plot_filename}'")
                    df3.write_html(plot_filename)

            except:
                logger.warning(
                    "Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )
                sys.exit(
                    "(Value Error): Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )

        elif plot == "sentiment":

            try:

                # loadies dependencies
                import plotly.graph_objects as go
                from textblob import TextBlob

                if topic_num is None:
                    logger.warning("topic_num set to None. Plot generated at corpus level.")
                    sentiments = data_[target_].map(
                        lambda text: TextBlob(text).sentiment.polarity
                    )
                    sentiments = pd.DataFrame(sentiments)
                    logger.info("Rendering Visual")

                    if display_format == "streamlit":
                        sentiments = sentiments[target_].iplot(
                            kind="hist",
                            bins=50,
                            xTitle="polarity",
                            linecolor="black",
                            yTitle="count",
                            title="Sentiment Polarity Distribution",
                            asFigure=True  # plotly obj needs to be returned for streamlit to interpret
                        )

                        st.write(sentiments)

                    else:
                        sentiments = sentiments[target_].iplot(
                            kind="hist",
                            bins=50,
                            xTitle="polarity",
                            linecolor="black",
                            yTitle="count",
                            title="Sentiment Polarity Distribution",
                            asFigure=save_param
                        )

                else:
                    title = str(topic_num) + ": " + "Sentiment Polarity Distribution"
                    logger.info(
                        "SubProcess assign_model() called =================================="
                    )
                    assigned_df = assign_model(model, verbose=False)
                    logger.info(
                        "SubProcess assign_model() end =================================="
                    )
                    filtered_df = assigned_df.loc[
                        assigned_df["Dominant_Topic"] == topic_num
                        ]
                    sentiments = filtered_df[target_].map(
                        lambda text: TextBlob(text).sentiment.polarity
                    )
                    sentiments = pd.DataFrame(sentiments)
                    logger.info("Rendering Visual")

                    if display_format == "streamlit":
                        sentiments = sentiments[target_].iplot(
                            kind="hist",
                            bins=50,
                            xTitle="polarity",
                            linecolor="black",
                            yTitle="count",
                            title=title,
                            asFigure=True  # plotly obj needs to be returned for streamlit to interpret
                        )

                        st.write(sentiments)

                    else:
                        sentiments = sentiments[target_].iplot(
                            kind="hist",
                            bins=50,
                            xTitle="polarity",
                            linecolor="black",
                            yTitle="count",
                            title=title,
                            asFigure=save_param
                        )

                logger.info("Visual Rendered Successfully")

                if save:
                    if not isinstance(save, bool):
                        plot_filename = os.path.join(save, "Sentiments.html")
                    else:
                        plot_filename = "Sentiments.html"
                    logger.info(f"Saving '{plot_filename}'")
                    sentiments.write_html(plot_filename)



            except:
                logger.warning(
                    "Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )
                sys.exit(
                    "(Value Error): Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )

        elif plot == "pos":

            from textblob import TextBlob

            b = list(id2word.token2id.keys())
            logger.info("Fitting TextBlob()")
            blob = TextBlob(str(b))
            pos_df = pd.DataFrame(blob.tags, columns=["word", "pos"])
            pos_df = pos_df.loc[pos_df["pos"] != "POS"]
            pos_df = pos_df.pos.value_counts()[:20]
            logger.info("Rendering Visual")

            if display_format == "streamlit":
                pos_df = pos_df.iplot(
                    kind="bar",
                    xTitle="POS",
                    yTitle="count",
                    title="Top 20 Part-of-speech tagging for review corpus",
                    asFigure=True  # plotly obj needs to be returned for streamlit to interpret
                )

                st.write(pos_df)

            else:
                pos_df = pos_df.iplot(
                    kind="bar",
                    xTitle="POS",
                    yTitle="count",
                    title="Top 20 Part-of-speech tagging for review corpus",
                    asFigure=save_param
                )

            logger.info("Visual Rendered Sucessfully")

            if save:
                if not isinstance(save, bool):
                    plot_filename = os.path.join(save, "POS.html")
                else:
                    plot_filename = "POS.html"
                logger.info(f"Saving '{plot_filename}'")
                pos_df.write_html(plot_filename)


        elif plot == "tsne":

            logger.info(
                "SubProcess assign_model() called =================================="
            )
            b = assign_model(model, verbose=False)
            logger.info("SubProcess assign_model() end ==================================")
            b.dropna(axis=0, inplace=True)  # droping rows where Dominant_Topic is blank

            c = []
            for i in b.columns:
                if "Topic_" in i:
                    a = i
                    c.append(a)

            bb = b[c]

            from sklearn.manifold import TSNE

            logger.info("Fitting TSNE()")
            X_embedded = TSNE(n_components=3).fit_transform(bb)

            logger.info("Sorting Dataframe")
            X = pd.DataFrame(X_embedded)
            X["Dominant_Topic"] = b["Dominant_Topic"]
            X.sort_values(by="Dominant_Topic", inplace=True)
            X.dropna(inplace=True)

            logger.info("Rendering Visual")
            import plotly.express as px

            df = X
            fig = px.scatter_3d(
                df,
                x=0,
                y=1,
                z=2,
                color="Dominant_Topic",
                title="3d TSNE Plot for Topic Model",
                opacity=0.7,
                width=900,
                height=800,
            )

            if system:
                if display_format == "streamlit":
                    st.write(fig)
                else:
                    fig.show()

            logger.info("Visual Rendered Successfully")

            if save:
                if not isinstance(save, bool):
                    plot_filename = os.path.join(save, "TSNE.html")
                else:
                    plot_filename = "TSNE.html"
                logger.info(f"Saving '{plot_filename}'")
                fig.write_html(plot_filename)


        elif plot == "topic_model":

            import pyLDAvis
            import pyLDAvis.gensim  # don't skip this

            import warnings

            warnings.filterwarnings("ignore")
            pyLDAvis.enable_notebook()
            logger.info("Preparing pyLDAvis visual")
            vis = pyLDAvis.gensim.prepare(model, corpus, id2word, mds="mmds")
            display(vis)
            logger.info("Visual Rendered Successfully")


        elif plot == "topic_distribution":

            try:

                iter1 = len(model.show_topics(999999))

            except:

                try:
                    iter1 = model.num_topics

                except:

                    iter1 = model.n_components_

            topic_name = []
            keywords = []

            for i in range(0, iter1):

                try:

                    s = model.show_topic(i, topn=10)
                    topic_name.append("Topic " + str(i))

                    kw = []

                    for i in s:
                        kw.append(i[0])

                    keywords.append(kw)

                except:

                    keywords.append("NA")
                    topic_name.append("Topic " + str(i))

            keyword = []
            for i in keywords:
                b = ", ".join(i)
                keyword.append(b)

            kw_df = pd.DataFrame({"Topic": topic_name, "Keyword": keyword}).set_index(
                "Topic"
            )
            logger.info(
                "SubProcess assign_model() called =================================="
            )
            ass_df = assign_model(model, verbose=False)
            logger.info("SubProcess assign_model() end ==================================")
            ass_df_pivot = ass_df.pivot_table(
                index="Dominant_Topic", values="Topic_0", aggfunc="count"
            )
            df2 = ass_df_pivot.join(kw_df)
            df2 = df2.reset_index()
            df2.columns = ["Topic", "Documents", "Keyword"]

            """
            sorting column starts

            """

            logger.info("Sorting Dataframe")

            topic_list = list(df2["Topic"])

            s = []
            for i in range(0, len(topic_list)):
                a = int(topic_list[i].split()[1])
                s.append(a)

            df2["Topic"] = s
            df2.sort_values(by="Topic", inplace=True)
            df2.sort_values(by="Topic", inplace=True)
            topic_list = list(df2["Topic"])
            topic_list = list(df2["Topic"])
            s = []
            for i in topic_list:
                a = "Topic " + str(i)
                s.append(a)

            df2["Topic"] = s
            df2.reset_index(drop=True, inplace=True)

            """
            sorting column ends
            """

            logger.info("Rendering Visual")

            import plotly.express as px

            fig = px.bar(
                df2,
                x="Topic",
                y="Documents",
                hover_data=["Keyword"],
                title="Document Distribution by Topics",
            )

            if system:
                if display_format == "streamlit":
                    st.write(fig)
                else:
                    fig.show()

            logger.info("Visual Rendered Successfully")

            if save:
                if not isinstance(save, bool):
                    plot_filename = os.path.join(save, "Topic Distribution.html")
                else:
                    plot_filename = "Topic Distribution.html"
                logger.info(f"Saving '{plot_filename}'")
                fig.write_html(plot_filename)

        elif plot == "wordcloud":

            try:

                from wordcloud import WordCloud, STOPWORDS
                import matplotlib.pyplot as plt

                stopwords = set(STOPWORDS)

                if topic_num is None:
                    logger.warning("topic_num set to None. Plot generated at corpus level.")
                    atext = " ".join(review for review in data_[target_])

                else:

                    logger.info(
                        "SubProcess assign_model() called =================================="
                    )
                    assigned_df = assign_model(model, verbose=False)
                    logger.info(
                        "SubProcess assign_model() end =================================="
                    )
                    filtered_df = assigned_df.loc[
                        assigned_df["Dominant_Topic"] == topic_num
                        ]
                    atext = " ".join(review for review in filtered_df[target_])

                logger.info("Fitting WordCloud()")
                wordcloud = WordCloud(
                    width=800,
                    height=800,
                    background_color="white",
                    stopwords=stopwords,
                    min_font_size=10,
                ).generate(atext)

                # plot the WordCloud image
                plt.figure(figsize=(8, 8), facecolor=None)
                plt.imshow(wordcloud)
                plt.axis("off")
                plt.tight_layout(pad=0)

                logger.info("Rendering Visual")

                if save or log_plots_param:
                    if system:
                        plt.savefig("Wordcloud.png")
                    else:
                        plt.savefig("Wordcloud.png")
                        plt.close()

                    logger.info("Saving 'Wordcloud.png' in current active directory")

                else:
                    if display_format == "streamlit":
                        st.write(plt)
                    else:
                        plt.show()

                logger.info("Visual Rendered Successfully")

            except:
                logger.warning(
                    "Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )
                sys.exit(
                    "(Value Error): Invalid topic_num param or empty Vocab. Try changing Topic Number."
                )

        elif plot == "umap":

            # warnings
            from matplotlib.axes._axes import _log as matplotlib_axes_logger

            matplotlib_axes_logger.setLevel("ERROR")

            # loading dependencies
            from sklearn.cluster import KMeans
            from sklearn.feature_extraction.text import TfidfVectorizer
            from yellowbrick.text import UMAPVisualizer
            import matplotlib.pyplot as plt

            tfidf = TfidfVectorizer()
            logger.info("Fitting TfidfVectorizer()")
            docs = tfidf.fit_transform(data_[target_])

            # Instantiate the clustering model_type
            clusters = KMeans(n_clusters=5, random_state=seed)
            logger.info("Fitting KMeans()")
            clusters.fit(docs)

            plt.figure(figsize=(10, 6))

            umap = UMAPVisualizer(random_state=seed)
            logger.info("Fitting UMAP()")
            umap.fit(docs, ["c{}".format(c) for c in clusters.labels_])

            logger.info("Rendering Visual")

            if save or log_plots_param:
                if system:
                    umap.show(outpath="UMAP.png")
                else:
                    umap.show(outpath="UMAP.png", clear_figure=True)

                logger.info("Saving 'UMAP.png' in current active directory")

            else:
                if display_format == "streamlit":
                    st.write(umap)
                else:
                    umap.show()

            logger.info("Visual Rendered Successfully")

        logger.info(
            "plot_model() succesfully completed......................................"
        )

    @classmethod
    def load(cls,
             model_dir=None,
             model_metadata=None,
             cached_component=None,
             **kwargs
             ):

        file_name = model_metadata.get("topic_file", TOPIC_MODEL_FILE_NAME)
        classifier_file = os.path.join(model_dir, file_name)
        import joblib
        if os.path.exists(classifier_file):
            model = joblib.load(classifier_file)

            return model
        else:
            return cls(model_metadata)

    def persist(self, model_dir):
        """Persist this model_type into the passed directory."""

        classifier_file = os.path.join(model_dir, TOPIC_MODEL_FILE_NAME)
        import joblib

        joblib.dump(self, classifier_file)

        return {"topic_file": TOPIC_MODEL_FILE_NAME}

    def tune_model(self,
            multi_core=False,
            supervised_target=None,
            estimator=None,
            optimize=None,
            custom_grid=None,
            auto_fe=True,
            fold=10,
            verbose=True,
    ):

        """
        This function tunes the ``num_topics`` parameter of a given model_type.

        model_type: str, default = None
            Enter ID of the models available in model_type library (ID - Model):

            * 'lda' - Latent Dirichlet Allocation
            * 'lsi' - Latent Semantic Indexing
            * 'hdp' - Hierarchical Dirichlet Process
            * 'rp' - Random Projections
            * 'nmf' - Non-Negative Matrix Factorization


        multi_core: bool, default = False
            True would utilize all CPU cores to parallelize and speed up model_type
            training. Ignored when ``model_type`` is not 'lda'.


        supervised_target: str
            Name of the target column for supervised learning. If None, the model_type
            coherence value is used as the objective function.


        estimator: str, default = None
            Classification (ID - Name):
                * 'lr' - Logistic Regression (Default)
                * 'knn' - K Nearest Neighbour
                * 'nb' - Naive Bayes
                * 'dt' - Decision Tree Classifier
                * 'svm' - SVM - Linear Kernel
                * 'rbfsvm' - SVM - Radial Kernel
                * 'gpc' - Gaussian Process Classifier
                * 'mlp' - Multi Level Perceptron
                * 'ridge' - Ridge Classifier
                * 'rf' - Random Forest Classifier
                * 'qda' - Quadratic Discriminant Analysis
                * 'ada' - Ada Boost Classifier
                * 'gbc' - Gradient Boosting Classifier
                * 'lda' - Linear Discriminant Analysis
                * 'et' - Extra Trees Classifier
                * 'xgboost' - Extreme Gradient Boosting
                * 'lightgbm' - Light Gradient Boosting
                * 'catboost' - CatBoost Classifier

            Regression (ID - Name):
                * 'lr' - Linear Regression (Default)
                * 'lasso' - Lasso Regression
                * 'ridge' - Ridge Regression
                * 'en' - Elastic Net
                * 'lar' - Least Angle Regression
                * 'llar' - Lasso Least Angle Regression
                * 'omp' - Orthogonal Matching Pursuit
                * 'br' - Bayesian Ridge
                * 'ard' - Automatic Relevance Determ.
                * 'par' - Passive Aggressive Regressor
                * 'ransac' - Random Sample Consensus
                * 'tr' - TheilSen Regressor
                * 'huber' - Huber Regressor
                * 'kr' - Kernel Ridge
                * 'svm' - Support Vector Machine
                * 'knn' - K Neighbors Regressor
                * 'dt' - Decision Tree
                * 'rf' - Random Forest
                * 'et' - Extra Trees Regressor
                * 'ada' - AdaBoost Regressor
                * 'gbr' - Gradient Boosting
                * 'mlp' - Multi Level Perceptron
                * 'xgboost' - Extreme Gradient Boosting
                * 'lightgbm' - Light Gradient Boosting
                * 'catboost' - CatBoost Regressor


        optimize: str, default = None
            For Classification tasks:
                Accuracy, AUC, Recall, Precision, F1, Kappa (default = 'Accuracy')

            For Regression tasks:
                MAE, MSE, RMSE, R2, RMSLE, MAPE (default = 'R2')


        custom_grid: list, default = None
            By default, a pre-defined number of topics is iterated over to
            optimize the supervised objective. To overwrite default iteration,
            pass a list of num_topics to iterate over in custom_grid param.


        auto_fe: bool, default = True
            Automatic text feature engineering. When set to True, it will generate
            text based features such as polarity, subjectivity, wordcounts. Ignored
            when ``supervised_target`` is None.


        fold: int, default = 10
            Number of folds to be used in Kfold CV. Must be at least 2.


        verbose: bool, default = True
            Status update is not printed when verbose is set to False.


        Returns:
            Trained Model with optimized ``num_topics`` parameter.


        Warnings
        --------
        - Random Projections ('rp') and Non Negative Matrix Factorization ('nmf')
          is not available for unsupervised learning. Error is raised when 'rp' or
          'nmf' is passed without supervised_target.

        - Estimators using kernel based methods such as Kernel Ridge Regressor,
          Automatic Relevance Determinant, Gaussian Process Classifier, Radial Basis
          Support Vector Machine and Multi Level Perceptron may have longer training
          times.


        """


        logger.info("Initializing tune_model()")
        logger.info(
            """tune_model(model_type={}, multi_core={}, supervised_target={}, estimator={}, optimize={}, custom_grid={}, auto_fe={}, fold={}, verbose={})""".format(
                str(self.model_type),
                str(multi_core),
                str(supervised_target),
                str(estimator),
                str(optimize),
                str(custom_grid),
                str(auto_fe),
                str(fold),
                str(verbose),
            )
        )

        logger.info("Checking exceptions")

        # ignore warnings
        import warnings

        warnings.filterwarnings("ignore")

        import sys

        # checking for model_type parameter
        if model is None:
            sys.exit(
                "(Value Error): Model parameter Missing. Please see docstring for list of available models."
            )

        # checking for allowed models
        allowed_models = ["lda", "lsi", "hdp", "rp", "nmf"]

        if model not in allowed_models:
            sys.exit(
                "(Value Error): Model Not Available. Please see docstring for list of available models."
            )

        # checking multicore type:
        if type(multi_core) is not bool:
            sys.exit(
                "(Type Error): multi_core parameter can only take argument as True or False."
            )

        # check supervised target:
        if supervised_target is not None:
            all_col = list(data_.columns)
            target = target_
            all_col.remove(target)
            if supervised_target not in all_col:
                sys.exit(
                    "(Value Error): supervised_target not recognized. It can only be one of the following: "
                    + str(all_col)
                )

        # supervised target exception handling
        if supervised_target is None:
            models_not_allowed = ["rp", "nmf"]

            if model in models_not_allowed:
                sys.exit(
                    "(Type Error): Model not supported for unsupervised tuning. Either supervised_target param has to be passed or different model_type has to be used. Please see docstring for available models."
                )

        # checking estimator:
        if estimator is not None:

            available_estimators = [
                "lr",
                "knn",
                "nb",
                "dt",
                "svm",
                "rbfsvm",
                "gpc",
                "mlp",
                "ridge",
                "rf",
                "qda",
                "ada",
                "gbc",
                "lda",
                "et",
                "lasso",
                "ridge",
                "en",
                "lar",
                "llar",
                "omp",
                "br",
                "ard",
                "par",
                "ransac",
                "tr",
                "huber",
                "kr",
                "svm",
                "knn",
                "dt",
                "rf",
                "et",
                "ada",
                "gbr",
                "mlp",
                "xgboost",
                "lightgbm",
                "catboost",
            ]

            if estimator not in available_estimators:
                sys.exit(
                    "(Value Error): Estimator Not Available. Please see docstring for list of available estimators."
                )

        # checking optimize parameter
        if optimize is not None:

            available_optimizers = [
                "MAE",
                "MSE",
                "RMSE",
                "R2",
                "ME",
                "Accuracy",
                "AUC",
                "Recall",
                "Precision",
                "F1",
                "Kappa",
            ]

            if optimize not in available_optimizers:
                sys.exit(
                    "(Value Error): optimize parameter Not Available. Please see docstring for list of available parameters."
                )

        # checking auto_fe:
        if type(auto_fe) is not bool:
            sys.exit(
                "(Type Error): auto_fe parameter can only take argument as True or False."
            )

        # checking fold parameter
        if type(fold) is not int:
            sys.exit("(Type Error): Fold parameter only accepts integer value.")

        """
        exception handling ends here
        """

        logger.info("Preloading libraries")

        # pre-load libraries
        import pandas as pd
        import ipywidgets as ipw
        from ipywidgets import Output
        from IPython.display import display, HTML, clear_output, update_display
        import datetime, time

        logger.info("Preparing display monitor")

        # progress bar
        if custom_grid is None:
            max_steps = 25
        else:
            max_steps = 10 + len(custom_grid)

        progress = ipw.IntProgress(
            value=0, min=0, max=max_steps, step=1, description="Processing: "
        )
        if verbose:
            if html_param:
                display(progress)

        timestampStr = datetime.datetime.now().strftime("%H:%M:%S")

        monitor = pd.DataFrame(
            [
                ["Initiated", ". . . . . . . . . . . . . . . . . .", timestampStr],
                ["Status", ". . . . . . . . . . . . . . . . . .", "Loading Dependencies"],
                ["Step", ". . . . . . . . . . . . . . . . . .", "Initializing"],
            ],
            columns=["", " ", "   "],
        ).set_index("")

        monitor_out = Output()

        if verbose:
            if html_param:
                display(monitor_out)

        if verbose:
            if html_param:
                with monitor_out:
                    display(monitor, display_id="monitor")

        logger.info("Importing libraries")

        # General Dependencies
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import cross_val_predict
        from sklearn import metrics
        import numpy as np
        import plotly.express as px

        # setting up cufflinks
        import cufflinks as cf

        cf.go_offline()
        cf.set_config_file(offline=False, world_readable=True)

        progress.value += 1

        # define the problem
        if supervised_target is None:
            problem = "unsupervised"
            logger.info("Objective : Unsupervised")
        elif data_[supervised_target].value_counts().count() == 2:
            problem = "classification"
            logger.info("Objective : Classification")
        else:
            problem = "regression"
            logger.info("Objective : Regression")

        # define topic_model_name
        logger.info("Defining model_type name")

        if model == "lda":
            topic_model_name = "Latent Dirichlet Allocation"
        elif model == "lsi":
            topic_model_name = "Latent Semantic Indexing"
        elif model == "hdp":
            topic_model_name = "Hierarchical Dirichlet Process"
        elif model == "nmf":
            topic_model_name = "Non-Negative Matrix Factorization"
        elif model == "rp":
            topic_model_name = "Random Projections"

        logger.info("Topic Model Name: " + str(topic_model_name))

        # defining estimator:
        logger.info("Defining supervised estimator")
        if problem == "classification" and estimator is None:
            estimator = "lr"
        elif problem == "regression" and estimator is None:
            estimator = "lr"
        else:
            estimator = estimator

        logger.info("Estimator: " + str(estimator))

        # defining optimizer:
        logger.info("Defining Optimizer")
        if optimize is None and problem == "classification":
            optimize = "Accuracy"
        elif optimize is None and problem == "regression":
            optimize = "R2"
        else:
            optimize = optimize

        logger.info("Optimize: " + str(optimize))

        progress.value += 1

        # creating sentiments

        if problem == "classification" or problem == "regression":

            logger.info("Problem : Supervised")

            if auto_fe:

                logger.info("auto_fe param set to True")

                monitor.iloc[1, 1:] = "Feature Engineering"
                if verbose:
                    if html_param:
                        update_display(monitor, display_id="monitor")

                from textblob import TextBlob

                monitor.iloc[2, 1:] = "Extracting Polarity"
                if verbose:
                    if html_param:
                        update_display(monitor, display_id="monitor")

                logger.info("Extracting Polarity")
                polarity = data_[target_].map(
                    lambda text: TextBlob(text).sentiment.polarity
                )

                monitor.iloc[2, 1:] = "Extracting Subjectivity"
                if verbose:
                    if html_param:
                        update_display(monitor, display_id="monitor")

                logger.info("Extracting Subjectivity")
                subjectivity = data_[target_].map(
                    lambda text: TextBlob(text).sentiment.subjectivity
                )

                monitor.iloc[2, 1:] = "Extracting Wordcount"
                if verbose:
                    if html_param:
                        update_display(monitor, display_id="monitor")

                logger.info("Extracting Wordcount")
                word_count = [len(i) for i in text]

                progress.value += 1

        # defining tuning grid
        logger.info("Defining Tuning Grid")

        if custom_grid is not None:
            logger.info("Custom Grid used")
            param_grid = custom_grid

        else:
            logger.info("Pre-defined Grid used")
            param_grid = [2, 4, 8, 16, 32, 64, 100, 200, 300, 400]

        master = []
        master_df = []

        monitor.iloc[1, 1:] = "Creating Topic Model"
        if verbose:
            if html_param:
                update_display(monitor, display_id="monitor")

        for i in param_grid:
            logger.info("Fitting Model with num_topics = " + str(i))
            progress.value += 1
            monitor.iloc[2, 1:] = "Fitting Model With " + str(i) + " Topics"
            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            # create and assign the model_type to dataset d
            logger.info(
                "SubProcess create_model() called =================================="
            )
            m = create_model(
                model=model, multi_core=multi_core, num_topics=i, verbose=False
            )
            logger.info("SubProcess create_model() end ==================================")

            logger.info(
                "SubProcess assign_model() called =================================="
            )
            d = assign_model(m, verbose=False)
            logger.info("SubProcess assign_model() end ==================================")

            if problem in ["classification", "regression"] and auto_fe:
                d["Polarity"] = polarity
                d["Subjectivity"] = subjectivity
                d["word_count"] = word_count

            master.append(m)
            master_df.append(d)

            # topic model_type creation end's here

        if problem == "unsupervised":

            logger.info("Problem : Unsupervised")

            monitor.iloc[1, 1:] = "Evaluating Topic Model"
            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            from gensim.models import CoherenceModel

            logger.info("CoherenceModel imported successfully")

            coherence = []
            metric = []

            counter = 0

            for i in master:
                logger.info("Evaluating Coherence with num_topics: " + str(i))
                progress.value += 1
                monitor.iloc[2, 1:] = (
                        "Evaluating Coherence With " + str(param_grid[counter]) + " Topics"
                )
                if verbose:
                    if html_param:
                        update_display(monitor, display_id="monitor")

                model = CoherenceModel(
                    model=i, texts=text, dictionary=id2word, coherence="c_v"
                )
                model_coherence = model.get_coherence()
                coherence.append(model_coherence)
                metric.append("Coherence")
                counter += 1

            monitor.iloc[1, 1:] = "Compiling Results"
            monitor.iloc[1, 1:] = "Finalizing"
            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            logger.info("Creating metrics dataframe")
            df = pd.DataFrame(
                {"# Topics": param_grid, "Score": coherence, "Metric": metric}
            )
            df.columns = ["# Topics", "Score", "Metric"]

            sorted_df = df.sort_values(by="Score", ascending=False)
            ival = sorted_df.index[0]

            best_model = master[ival]
            best_model_df = master_df[ival]

            logger.info("Rendering Visual")
            fig = px.line(
                df,
                x="# Topics",
                y="Score",
                line_shape="linear",
                title="Coherence Value and # of Topics",
                color="Metric",
            )

            fig.update_layout(plot_bgcolor="rgb(245,245,245)")

            fig.show()
            logger.info("Visual Rendered Successfully")

            # monitor = ''

            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            monitor_out.clear_output()
            progress.close()

            best_k = np.array(sorted_df.head(1)["# Topics"])[0]
            best_m = round(np.array(sorted_df.head(1)["Score"])[0], 4)
            p = (
                    "Best Model: "
                    + topic_model_name
                    + " |"
                    + " # Topics: "
                    + str(best_k)
                    + " | "
                    + "Coherence: "
                    + str(best_m)
            )
            print(p)

        elif problem == "classification":

            logger.info("Importing untrained Classifier")

            """

            defining estimator

            """

            monitor.iloc[1, 1:] = "Evaluating Topic Model"
            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            if estimator == "lr":

                from sklearn.linear_model import LogisticRegression

                model = LogisticRegression(random_state=seed)
                full_name = "Logistic Regression"

            elif estimator == "knn":

                from sklearn.neighbors import KNeighborsClassifier

                model = KNeighborsClassifier()
                full_name = "K Nearest Neighbours"

            elif estimator == "nb":

                from sklearn.naive_bayes import GaussianNB

                model = GaussianNB()
                full_name = "Naive Bayes"

            elif estimator == "dt":

                from sklearn.tree import DecisionTreeClassifier

                model = DecisionTreeClassifier(random_state=seed)
                full_name = "Decision Tree"

            elif estimator == "svm":

                from sklearn.linear_model import SGDClassifier

                model = SGDClassifier(max_iter=1000, tol=0.001, random_state=seed)
                full_name = "Support Vector Machine"

            elif estimator == "rbfsvm":

                from sklearn.svm import SVC

                model = SVC(
                    gamma="auto", C=1, probability=True, kernel="rbf", random_state=seed
                )
                full_name = "RBF SVM"

            elif estimator == "gpc":

                from sklearn.gaussian_process import GaussianProcessClassifier

                model = GaussianProcessClassifier(random_state=seed)
                full_name = "Gaussian Process Classifier"

            elif estimator == "mlp":

                from sklearn.neural_network import MLPClassifier

                model = MLPClassifier(max_iter=500, random_state=seed)
                full_name = "Multi Level Perceptron"

            elif estimator == "ridge":

                from sklearn.linear_model import RidgeClassifier

                model = RidgeClassifier(random_state=seed)
                full_name = "Ridge Classifier"

            elif estimator == "rf":

                from sklearn.ensemble import RandomForestClassifier

                model = RandomForestClassifier(n_estimators=10, random_state=seed)
                full_name = "Random Forest Classifier"

            elif estimator == "qda":

                from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

                model = QuadraticDiscriminantAnalysis()
                full_name = "Quadratic Discriminant Analysis"

            elif estimator == "ada":

                from sklearn.ensemble import AdaBoostClassifier

                model = AdaBoostClassifier(random_state=seed)
                full_name = "AdaBoost Classifier"

            elif estimator == "gbc":

                from sklearn.ensemble import GradientBoostingClassifier

                model = GradientBoostingClassifier(random_state=seed)
                full_name = "Gradient Boosting Classifier"

            elif estimator == "lda":

                from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

                model = LinearDiscriminantAnalysis()
                full_name = "Linear Discriminant Analysis"

            elif estimator == "et":

                from sklearn.ensemble import ExtraTreesClassifier

                model = ExtraTreesClassifier(random_state=seed)
                full_name = "Extra Trees Classifier"

            elif estimator == "xgboost":

                from xgboost import XGBClassifier

                model = XGBClassifier(random_state=seed, n_jobs=-1, verbosity=0)
                full_name = "Extreme Gradient Boosting"

            elif estimator == "lightgbm":

                import lightgbm as lgb

                model = lgb.LGBMClassifier(random_state=seed)
                full_name = "Light Gradient Boosting Machine"

            elif estimator == "catboost":
                from catboost import CatBoostClassifier

                model = CatBoostClassifier(
                    random_state=seed, silent=True
                )  # Silent is True to suppress CatBoost iteration results
                full_name = "CatBoost Classifier"

            logger.info(str(full_name) + " Imported Successfully")

            progress.value += 1

            """
            start model_type building here

            """

            acc = []
            auc = []
            recall = []
            prec = []
            kappa = []
            f1 = []

            for i in range(0, len(master_df)):
                progress.value += 1
                param_grid_val = param_grid[i]

                logger.info(
                    "Training supervised model_type with num_topics: " + str(param_grid_val)
                )

                monitor.iloc[2, 1:] = (
                        "Evaluating Classifier With " + str(param_grid_val) + " Topics"
                )
                if verbose:
                    if html_param:
                        update_display(monitor, display_id="monitor")

                # prepare the dataset for supervised problem
                d = master_df[i]
                d.dropna(axis=0, inplace=True)  # droping rows where Dominant_Topic is blank
                d.drop([target_], inplace=True, axis=1)
                d = pd.get_dummies(d)

                # split the dataset
                X = d.drop(supervised_target, axis=1)
                y = d[supervised_target]

                # fit the model_type
                logger.info("Fitting Model")
                model.fit(X, y)

                # generate the prediction and evaluate metric
                logger.info("Generating Cross Val Predictions")
                pred = cross_val_predict(model, X, y, cv=fold, method="predict")

                acc_ = metrics.accuracy_score(y, pred)
                acc.append(acc_)

                recall_ = metrics.recall_score(y, pred)
                recall.append(recall_)

                precision_ = metrics.precision_score(y, pred)
                prec.append(precision_)

                kappa_ = metrics.cohen_kappa_score(y, pred)
                kappa.append(kappa_)

                f1_ = metrics.f1_score(y, pred)
                f1.append(f1_)

                if hasattr(model, "predict_proba"):
                    pred_ = cross_val_predict(model, X, y, cv=fold, method="predict_proba")
                    pred_prob = pred_[:, 1]
                    auc_ = metrics.roc_auc_score(y, pred_prob)
                    auc.append(auc_)

                else:
                    auc.append(0)

            monitor.iloc[1, 1:] = "Compiling Results"
            monitor.iloc[1, 1:] = "Finalizing"
            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            logger.info("Creating metrics dataframe")
            df = pd.DataFrame(
                {
                    "# Topics": param_grid,
                    "Accuracy": acc,
                    "AUC": auc,
                    "Recall": recall,
                    "Precision": prec,
                    "F1": f1,
                    "Kappa": kappa,
                }
            )

            sorted_df = df.sort_values(by=optimize, ascending=False)
            ival = sorted_df.index[0]

            best_model = master[ival]
            best_model_df = master_df[ival]
            progress.value += 1

            logger.info("Rendering Visual")
            sd = pd.melt(
                df,
                id_vars=["# Topics"],
                value_vars=["Accuracy", "AUC", "Recall", "Precision", "F1", "Kappa"],
                var_name="Metric",
                value_name="Score",
            )

            fig = px.line(
                sd,
                x="# Topics",
                y="Score",
                color="Metric",
                line_shape="linear",
                range_y=[0, 1],
            )
            fig.update_layout(plot_bgcolor="rgb(245,245,245)")
            title = str(full_name) + " Metrics and # of Topics"
            fig.update_layout(
                title={
                    "text": title,
                    "y": 0.95,
                    "x": 0.45,
                    "xanchor": "center",
                    "yanchor": "top",
                }
            )

            fig.show()
            logger.info("Visual Rendered Successfully")

            # monitor = ''

            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            monitor_out.clear_output()
            progress.close()

            best_k = np.array(sorted_df.head(1)["# Topics"])[0]
            best_m = round(np.array(sorted_df.head(1)[optimize])[0], 4)
            p = (
                    "Best Model: "
                    + topic_model_name
                    + " |"
                    + " # Topics: "
                    + str(best_k)
                    + " | "
                    + str(optimize)
                    + " : "
                    + str(best_m)
            )
            print(p)

        elif problem == "regression":

            logger.info("Importing untrained Regressor")

            """

            defining estimator

            """

            monitor.iloc[1, 1:] = "Evaluating Topic Model"
            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            if estimator == "lr":

                from sklearn.linear_model import LinearRegression

                model = LinearRegression()
                full_name = "Linear Regression"

            elif estimator == "lasso":

                from sklearn.linear_model import Lasso

                model = Lasso(random_state=seed)
                full_name = "Lasso Regression"

            elif estimator == "ridge":

                from sklearn.linear_model import Ridge

                model = Ridge(random_state=seed)
                full_name = "Ridge Regression"

            elif estimator == "en":

                from sklearn.linear_model import ElasticNet

                model = ElasticNet(random_state=seed)
                full_name = "Elastic Net"

            elif estimator == "lar":

                from sklearn.linear_model import Lars

                model = Lars()
                full_name = "Least Angle Regression"

            elif estimator == "llar":

                from sklearn.linear_model import LassoLars

                model = LassoLars()
                full_name = "Lasso Least Angle Regression"

            elif estimator == "omp":

                from sklearn.linear_model import OrthogonalMatchingPursuit

                model = OrthogonalMatchingPursuit()
                full_name = "Orthogonal Matching Pursuit"

            elif estimator == "br":
                from sklearn.linear_model import BayesianRidge

                model = BayesianRidge()
                full_name = "Bayesian Ridge Regression"

            elif estimator == "ard":

                from sklearn.linear_model import ARDRegression

                model = ARDRegression()
                full_name = "Automatic Relevance Determination"

            elif estimator == "par":

                from sklearn.linear_model import PassiveAggressiveRegressor

                model = PassiveAggressiveRegressor(random_state=seed)
                full_name = "Passive Aggressive Regressor"

            elif estimator == "ransac":

                from sklearn.linear_model import RANSACRegressor

                model = RANSACRegressor(random_state=seed)
                full_name = "Random Sample Consensus"

            elif estimator == "tr":

                from sklearn.linear_model import TheilSenRegressor

                model = TheilSenRegressor(random_state=seed)
                full_name = "TheilSen Regressor"

            elif estimator == "huber":

                from sklearn.linear_model import HuberRegressor

                model = HuberRegressor()
                full_name = "Huber Regressor"

            elif estimator == "kr":

                from sklearn.kernel_ridge import KernelRidge

                model = KernelRidge()
                full_name = "Kernel Ridge"

            elif estimator == "svm":

                from sklearn.svm import SVR

                model = SVR()
                full_name = "Support Vector Regression"

            elif estimator == "knn":

                from sklearn.neighbors import KNeighborsRegressor

                model = KNeighborsRegressor()
                full_name = "Nearest Neighbors Regression"

            elif estimator == "dt":

                from sklearn.tree import DecisionTreeRegressor

                model = DecisionTreeRegressor(random_state=seed)
                full_name = "Decision Tree Regressor"

            elif estimator == "rf":

                from sklearn.ensemble import RandomForestRegressor

                model = RandomForestRegressor(random_state=seed)
                full_name = "Random Forest Regressor"

            elif estimator == "et":

                from sklearn.ensemble import ExtraTreesRegressor

                model = ExtraTreesRegressor(random_state=seed)
                full_name = "Extra Trees Regressor"

            elif estimator == "ada":

                from sklearn.ensemble import AdaBoostRegressor

                model = AdaBoostRegressor(random_state=seed)
                full_name = "AdaBoost Regressor"

            elif estimator == "gbr":

                from sklearn.ensemble import GradientBoostingRegressor

                model = GradientBoostingRegressor(random_state=seed)
                full_name = "Gradient Boosting Regressor"

            elif estimator == "mlp":

                from sklearn.neural_network import MLPRegressor

                model = MLPRegressor(random_state=seed)
                full_name = "MLP Regressor"

            elif estimator == "xgboost":

                from xgboost import XGBRegressor

                model = XGBRegressor(random_state=seed, n_jobs=-1, verbosity=0)
                full_name = "Extreme Gradient Boosting Regressor"

            elif estimator == "lightgbm":

                import lightgbm as lgb

                model = lgb.LGBMRegressor(random_state=seed)
                full_name = "Light Gradient Boosting Machine"

            elif estimator == "catboost":
                from catboost import CatBoostRegressor

                model = CatBoostRegressor(random_state=seed, silent=True)
                full_name = "CatBoost Regressor"

            logger.info(str(full_name) + " Imported Successfully")

            progress.value += 1

            """
            start model_type building here

            """

            score = []
            metric = []

            for i in range(0, len(master_df)):
                progress.value += 1
                param_grid_val = param_grid[i]

                logger.info(
                    "Training supervised model_type with num_topics: " + str(param_grid_val)
                )

                monitor.iloc[2, 1:] = (
                        "Evaluating Regressor With " + str(param_grid_val) + " Topics"
                )
                if verbose:
                    if html_param:
                        update_display(monitor, display_id="monitor")

                # prepare the dataset for supervised problem
                d = master_df[i]
                d.dropna(axis=0, inplace=True)  # droping rows where Dominant_Topic is blank
                d.drop([target_], inplace=True, axis=1)
                d = pd.get_dummies(d)

                # split the dataset
                X = d.drop(supervised_target, axis=1)
                y = d[supervised_target]

                # fit the model_type
                logger.info("Fitting Model")
                model.fit(X, y)

                # generate the prediction and evaluate metric
                logger.info("Generating Cross Val Predictions")
                pred = cross_val_predict(model, X, y, cv=fold, method="predict")

                if optimize == "R2":
                    r2_ = metrics.r2_score(y, pred)
                    score.append(r2_)

                elif optimize == "MAE":
                    mae_ = metrics.mean_absolute_error(y, pred)
                    score.append(mae_)

                elif optimize == "MSE":
                    mse_ = metrics.mean_squared_error(y, pred)
                    score.append(mse_)

                elif optimize == "RMSE":
                    mse_ = metrics.mean_squared_error(y, pred)
                    rmse_ = np.sqrt(mse_)
                    score.append(rmse_)

                elif optimize == "ME":
                    max_error_ = metrics.max_error(y, pred)
                    score.append(max_error_)

                metric.append(str(optimize))

            monitor.iloc[1, 1:] = "Compiling Results"
            monitor.iloc[1, 1:] = "Finalizing"
            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            logger.info("Creating metrics dataframe")
            df = pd.DataFrame({"# Topics": param_grid, "Score": score, "Metric": metric})
            df.columns = ["# Topics", optimize, "Metric"]

            # sorting to return best model_type
            if optimize == "R2":
                sorted_df = df.sort_values(by=optimize, ascending=False)
            else:
                sorted_df = df.sort_values(by=optimize, ascending=True)

            ival = sorted_df.index[0]

            best_model = master[ival]
            best_model_df = master_df[ival]

            logger.info("Rendering Visual")

            fig = px.line(
                df,
                x="# Topics",
                y=optimize,
                line_shape="linear",
                title=str(full_name) + " Metrics and # of Topics",
                color="Metric",
            )

            fig.update_layout(plot_bgcolor="rgb(245,245,245)")

            progress.value += 1

            # monitor = ''

            if verbose:
                if html_param:
                    update_display(monitor, display_id="monitor")

            monitor_out.clear_output()
            progress.close()

            fig.show()
            logger.info("Visual Rendered Successfully")

            best_k = np.array(sorted_df.head(1)["# Topics"])[0]
            best_m = round(np.array(sorted_df.head(1)[optimize])[0], 4)
            p = (
                    "Best Model: "
                    + topic_model_name
                    + " |"
                    + " # Topics: "
                    + str(best_k)
                    + " | "
                    + str(optimize)
                    + " : "
                    + str(best_m)
            )
            print(p)

        logger.info(str(best_model))
        logger.info(
            "tune_model() succesfully completed......................................"
        )

        return best_model

    def evaluate_model(self):

        """
        This function displays a user interface for analyzing performance of a trained
        model_type. It calls the ``plot_model`` function internally.


        Example
        -------
        >>> from pycaret.datasets import get_data
        >>> kiva = get_data('kiva')
        >>> experiment_name = setup(data = kiva, target = 'en')
        >>> lda = create_model('lda')
        >>> evaluate_model(lda)


        model_type: object, default = none
            A trained model_type object should be passed.


        Returns:
            None

        """

        from ipywidgets import widgets
        from ipywidgets.widgets import interact, fixed, interact_manual
        import numpy as np

        """
        generate sorted list

        """

        try:
            n_topic_assigned = len(model.show_topics())
        except:
            try:
                n_topic_assigned = model.num_topics
            except:
                n_topic_assigned = model.n_components

        final_list = []
        for i in range(0, n_topic_assigned):
            final_list.append("Topic " + str(i))

        a = widgets.ToggleButtons(
            options=[
                ("Frequency Plot", "frequency"),
                ("Bigrams", "bigram"),
                ("Trigrams", "trigram"),
                ("Sentiment Polarity", "sentiment"),
                ("Word Cloud", "wordcloud"),
            ],
            description="Plot Type:",
            disabled=False,
            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
            icons=[""],
        )

        b = widgets.Dropdown(options=final_list, description="Topic #:", disabled=False)

        d = interact_manual(
            plot_model,
            model=fixed(model),
            plot=a,
            topic_num=b,
            save=fixed(False),
            system=fixed(True),
            display_format=fixed(None),
        )


def get_available_models():

    """
    Returns table of models available in model_type library.


    Example
    -------
    >>> from kolibri.task.clustering import get_available_models
    >>> all_models = available_models()


    Returns:
        pandas.DataFrame

    """

    import pandas as pd

    model_id = ["lda", "lda", "lsi", "hdp", "rp", "nmf"]

    algorithms=["variational", "gibbs", None, None, None, None]
    model_name = [
        "Latent Dirichlet Allocation",
        "Latent Dirichlet Allocation",
        "Latent Semantic Indexing",
        "Hierarchical Dirichlet Process",
        "Random Projections",
        "Non-Negative Matrix Factorization",
    ]


    df = pd.DataFrame({"ID": model_id, "algorithm": algorithms, "Name": model_name})

    df.set_index("ID", inplace=True)

    return df


from kolibri.registry import ModulesRegistry
ModulesRegistry.add_module(TopicModel.name, TopicModel)
