import unittest
import lumipy as lm
from sklearn.datasets import load_iris, load_digits, load_diabetes
import pandas as pd
import lumipy.provider as lp
from test.test_utils import load_secrets_into_env_if_local_run
import time
import requests as r
from os.path import exists
from lumipy.provider.thread import get_factory_dll_path
import numpy as np


class TestPythonProviderIntegration(unittest.TestCase):

    def setUp(self) -> None:

        load_secrets_into_env_if_local_run()

        def get_df_from_load_fn(load_fn):
            data = load_fn(as_frame=True)
            return pd.concat([data['data'], data['target']], axis=1)

        self.test_dfs = {
            "Test": pd.DataFrame([{"A": i, "B": i**2, "C": i**0.5} for i in range(25)]),
            "Iris": get_df_from_load_fn(load_iris),
            "Diabetes": get_df_from_load_fn(load_diabetes),
            "Digits": get_df_from_load_fn(load_digits),
        }

        providers = []
        # Add pandas providers
        for name, df in self.test_dfs.items():
            providers.append(lp.PandasProvider(df, name))
        # 2D multivariate Gaussian provider
        providers.append(lp.GaussianDistProvider(dimensions=2))
        # PCA projection provider
        providers.append(lp.PcaProjectionProvider(n_components=2))

        # Build server but don't start it
        self.server = lp.ProviderManager(providers)

    @unittest.skipIf(
        not exists(get_factory_dll_path()),
        "Experimental feature: will only run if the factory dll is present."
    )
    def test_local_python_pandas_provider_integration(self):

        # Start server in with block...
        with self.server:

            # Wait a bit for the factory to set everything up. This is not blocking the start of
            # the with block because it's running in the background.
            time.sleep(20)

            # Should now be set up - get the atlas...
            atlas = lm.get_atlas()

            # Test that the providers are there
            for name in self.test_dfs.keys():
                self.assertTrue(
                    hasattr(atlas, f'pandas_{name.lower()}'),
                    msg=f'Pandas.{name} was not found in the atlas: factory may not have started, '
                        f'or provider may have failed to be registered.'
                )

            # Test that they return data for simple query (select * limit 10)
            for name, df in self.test_dfs.items():
                cls = getattr(atlas, f'pandas_{name.lower()}')
                p = cls()
                res = p.select('*').limit(10).go()
                self.assertEqual(res.shape[0], 10)
                self.assertEqual(res.shape[1], df.shape[1])

        time.sleep(10)

        # Shutdown asserts
        # There should no longer be a web server.
        with self.assertRaises(Exception) as e:
            res = r.get('http://localhost:5000')
            res.raise_for_status()

        # There should no longer be pandas providers on the luminesce grid.
        # Rebuild the atlas
        atlas = lm.get_atlas()
        # and assert that the provider are not there
        for name in self.test_dfs.keys():
            self.assertFalse(
                hasattr(atlas, f'pandas_{name.lower()}'),
                msg=f'Pandas.{name} was found in the post-shutdown atlas: factory may not have been shutdown properly'
            )

    @unittest.skipIf(
        not exists(get_factory_dll_path()),
        "Experimental feature: will only run if the factory dll is present."
    )
    def test_local_2d_gaussian_dist_provider(self):

        # Start server in with block...
        with self.server:

            # Wait a bit for the factory to set everything up. This is not blocking the start of
            # the with block because it's running in the background.
            time.sleep(20)

            # Should now be set up - get the atlas...
            atlas = lm.get_atlas()

            # Define covariance matrix and mean vector
            covmat = [[2, -1], [-1, 1]]
            means = [1, -1]

            # Build covariance matrix and means table vars
            covmat_tv = lm.from_array(covmat)
            means_tv = lm.from_array(means)

            # Build 2D gaussian provider with the above values and query it
            gauss2d = atlas.numpy_random_gaussian2d(
                covariance=covmat_tv,
                means=means_tv,
                num_draws=5000
            )
            qry = gauss2d.select('*')
            g2d_df = qry.go()

            # DF should be the right shape: 5000 draws with two dimensions each
            self.assertEqual(g2d_df.shape[0], 5000)
            self.assertEqual(g2d_df.shape[1], 2)

            # Assert that the measured covariance matrix is approximately equal to the input one.
            obs_covmat = g2d_df.cov().round().values
            self.assertTrue((obs_covmat == np.array(covmat)).all())

    @unittest.skipIf(
        not exists(get_factory_dll_path()),
        "Experimental feature: will only run if the factory dll is present."
    )
    def test_providers_together(self):

        # Start server in with block...
        with self.server:

            # Wait a bit for the factory to set everything up. This is not blocking the start of
            # the with block because it's running in the background.
            time.sleep(20)

            # Should now be set up - get the atlas...
            atlas = lm.get_atlas()

            # Digits provider as a table variable
            digits = atlas.pandas_digits().select('*').to_table_var()

            # Feed into the PCA projector which will compute the principal components and then project the data in the
            # table variable on to the top two principal components.
            pca2d = atlas.sklearn_pca_projector2d(input_data=digits)
            pca_df = pca2d.select('*').go()

            # Should be one row for each row in the digits dataset
            self.assertEqual(pca_df.shape[0], self.test_dfs['Digits'].shape[0])
            # With two dimensions each - one per principal component.
            self.assertEqual(pca_df.shape[1], 2)
