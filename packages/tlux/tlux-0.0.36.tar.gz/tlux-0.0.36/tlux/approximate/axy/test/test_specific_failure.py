
from tlux.plot import Plot
from tlux.approximate.axy.test.scenarios import (
    scenarios,
    AXY,
    Details,
    check_code,
    spawn_model,
    gen_config_data,
    scenario_generator
)

import numpy as np
np.set_printoptions(linewidth=100)


        # import pickle, os
        # with open(os.path.expanduser('~/Git/tlux/tlux/approximate/axy/test/bad-config-data.pkl'), 'wb') as f:
        #     pickle.dump(dict(
        #         config = self.config,
        #         model = self.model,
        #         rwork = rwork,
        #         iwork = iwork,
        #         ax_in = ax.T,
        #         axi_in = axi.T,
        #         sizes_in = sizes,
        #         x_in = x.T,
        #         xi_in = xi.T,
        #         y_in = y.T,
        #         yw_in = yw.T,
        #         steps = steps,
        #         record = self.record.T
        #     ), f)


def _test_specific_failure():
    # from tlux.approximate.axy import AXY
    # path = "temp-data-failure.pkl"
    # import pickle, os
    # with open(path, 'rb') as f:
    #     fit_kwargs = pickle.load(f)
    # model = AXY()
    # model.fit(**fit_kwargs)

    import pickle, os
    # path = "bad-config-data.pkl"
    path = "sample-nan-data.pkl"
    with open(path, 'rb') as f:
        fit_kwargs = pickle.load(f)
    print()
    for (k,v) in fit_kwargs.items():
        print(k, type(v).__name__, (v.shape if hasattr(v, 'shape') else v))
    print()
    # Convert some arguments into a "Details" object for easier introspection.
    details = Details(config=fit_kwargs['config'], steps=fit_kwargs['steps'])
    config = details.config
    fit_kwargs['model'] = details.model
    fit_kwargs['rwork'] = details.rwork
    fit_kwargs['iwork'] = details.iwork
    fit_kwargs['record'] = details.record
    fit_kwargs['config'].step_emb_change = 0.05
    fit_kwargs['config'].log_grad_norm_frequency = 1
    fit_kwargs['config'].axi_normalized = False
    fit_kwargs['config'].xi_normalized = False
    fit_kwargs['config'].early_stop = False
    # fit_kwargs['steps'] = 400
    fit_kwargs['config'].step_factor = 0.001

    # Re initialize the model.
    AXY.init_model(fit_kwargs['config'], fit_kwargs['model'], seed=0)

    print("np.any(np.isnan(details.x_in)): ", np.any(np.isnan(fit_kwargs['x_in'])))

    from tlux.math import svd
    from tlux.plot import Plot
    p = Plot()

    axi = details.a_embeddings.T
    vals, vecs = svd(axi)
    print("vals: ", vals)
    axi = axi @ (vecs[:3].T)
    p.add('axi before', *axi.T, marker_size=2)
    # p.add('y before', *fit_kwargs['y_in'], marker_size=2)

    (
        config,
        model,
        rwork,
        iwork,
        ax_in,
        x_in, 
        y_in,
        yw_in,
        record,
        sse,
        info
    ) = AXY.fit_model(
        **fit_kwargs
    )

    print()

    axi = details.a_embeddings.T
    vals, vecs = svd(axi)
    print("vals: ", vals)
    axi = axi @ (vecs[:3].T)
    p.add('axi after', *axi.T, marker_size=2)

    # p.add('y after', *y_in, marker_size=2)
    p.show(show=False)

    p = Plot()
    record = record.T
    steps = list(range(1,len(record)+1))
    p.add("MSE", steps, record[:,0], mode="lines")
    p.add("Step factor", steps, record[:,1], mode="lines")
    p.add("Step norm", steps, record[:,2], mode="lines")
    p.add("Update ratio", steps, record[:,3], mode="lines")
    # p.add("Eval rank", steps, record[:,4], mode="lines")
    # p.add("Grad rank", steps, record[:,5], mode="lines")
    p.show(append=True)

    exit()

    # print("np.any(np.isnan(details.x_in)): ", np.any(np.isnan(x_in)))

    # print("details.x.shape: ", details.x.shape)
    # print("details.x: ", details.x)
    # rows = np.arange(details.x.shape[1])[np.any(np.isnan(details.x.T), axis=1)]
    # print("rows: ", rows)
    # print("details.x[rows]: ", details.x.T[rows])
    # print()
    # for i in rows:
    #     print(i, details.x[:,i].tolist())
    # print()
    # print("np.arange(details.x.size).reshape(details.x.shape)[np.isnan(details.x)]: \n", np.arange(details.x.size).reshape(details.x.shape)[np.isnan(details.x)])
    # print("np.any(np.isnan(details.x)): ", np.any(np.isnan(details.x)))
    # print()

    # print("fit_kwargs['xi'].shape: ", fit_kwargs['xi_in'].shape)
    # print("details.m_embeddings: ", details.m_embeddings.T)
    # print("set(fit_kwargs['xi_in'].flatten().tolist()): ", set(fit_kwargs['xi_in'].flatten().tolist()))
    # print("config.mne: ", config.mne)
    # print("config.mde: ", config.mde)
    # print("np.any(np.isnan(details.y_grad)): ", np.any(np.isnan(details.y_grad)))
    # print("np.any(np.isnan(details.model_grads)): ", np.any(np.isnan(details.model_grads)))
    # print("np.any(np.isnan(details.agg_grads)): ", np.any(np.isnan(details.agg_grads)))

    # p.add('y after', *y_in, marker_size=2)
    # from tlux.math import svd
    # ax = details.ax[config.adn:,:]
    # print("config.adn: ", config.adn)
    # print("config.adi: ", config.adi)
    # print("ax.shape: ", ax.shape)
    # vals, vecs = svd(ax.T)
    # print("vals: ", vals)
    # print("vecs.shape: ", vecs.shape)
    # exit()
    # p.add()
    # p.show()


    print("sse: ", sse)
    print("y_in.shape: ", y_in.shape)
    check_code(info, 'fit_model')


_test_specific_failure()
exit()

