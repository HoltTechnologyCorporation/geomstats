"""Unit tests for embedding data class."""

import geomstats.backend as gs
from geomstats.datasets.utils import load_karate_graph
from geomstats.geometry.poincare_ball import PoincareBall
from geomstats.learning.embedding_data import Embedding
import geomstats.tests

class TestDatasets(geomstats.tests.TestCase):

    def setUp(self):

        gs.random.seed(1234)
        dim = 2
        max_epochs = 3
        lr = .05
        n_negative = 2
        context_size = 1
        karate_graph = load_karate_graph()

        self.hyperbolic_manifold = PoincareBall(2)

        self.embedding_class = Embedding(data=karate_graph,
                                    manifold=self.hyperbolic_manifold,
                                    dim=dim,
                                    max_epochs=max_epochs,
                                    lr=lr,
                                    n_negative=n_negative,
                                    context_size=context_size)

    def test_log_sigmoid(self):

        point = gs.array([0.1, 0.3])
        result = self.embedding_class.log_sigmoid(point)

        expected = gs.array([-0.644397, -0.554355])
        self.assertAllClose(result, expected)

    def test_grad_log_sigmoid(self):

        point = gs.array([0.1, 0.3])
        result = self.embedding_class.grad_log_sigmoid(point)

        expected = gs.array([0.47502081, 0.42555748])
        self.assertAllClose(result, expected)

    def test_loss(self):
        point = gs.array([0.5, 0.5])
        point_context = gs.array([0.6, 0.6])
        point_negative = gs.array([-0.4, -0.4])

        loss_value, loss_grad = self.embedding_class.loss(
            point, point_context, point_negative)

        expected_loss = 1.00322045
        expected_grad = gs.array([[-0.16565083, -0.16565083]])

        self.assertAllClose(loss_value, expected_loss, rtol = 1e-3)
        self.assertAllClose(loss_grad, expected_grad, rtol = 1e-3)

    def test_embed(self):

        embeddings = self.embedding_class.embed()

        self.assertTrue(self.hyperbolic_manifold.belongs(embeddings).all())