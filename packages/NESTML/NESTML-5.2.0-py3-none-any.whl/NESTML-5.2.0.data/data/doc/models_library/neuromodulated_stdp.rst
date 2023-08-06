neuromodulated_stdp
###################


neuromodulated_stdp - Synapse model for spike-timing dependent plasticity modulated by a neurotransmitter such as dopamine

Description
+++++++++++
stdp_dopamine_synapse is a connection to create synapses with
dopamine-modulated spike-timing dependent plasticity (used as a
benchmark model in [1]_, based on [2]_). The dopaminergic signal is a
low-pass filtered version of the spike rate of a user-specific pool
of neurons. The spikes emitted by the pool of dopamine neurons are
delivered to the synapse via the assigned volume transmitter. The
dopaminergic dynamics is calculated in the synapse itself.



Parameters
++++++++++



.. csv-table::
    :header: "Name", "Physical unit", "Default value", "Description"
    :widths: auto

    
    "the_delay", "ms", "1ms", "!!! cannot have a variable called ""delay"""    
    "tau_tr_pre", "ms", "20ms", "STDP time constant for weight changes caused by pre-before-post spike pairings."    
    "tau_tr_post", "ms", "20ms", "STDP time constant for weight changes caused by post-before-pre spike pairings."    
    "tau_c", "ms", "1000ms", "Time constant of eligibility trace"    
    "tau_n", "ms", "200ms", "Time constant of dopaminergic trace"    
    "b", "real", "0.0", "Dopaminergic baseline concentration"    
    "Wmax", "real", "200.0", "Maximal synaptic weight"    
    "Wmin", "real", "0.0", "Minimal synaptic weight"    
    "A_plus", "real", "1.0", "Multiplier applied to weight changes caused by pre-before-post spike pairings. If b (dopamine baseline concentration) is zero, then A_plus is simply the multiplier for facilitation (as in the stdp_synapse model). If b is not zero, then A_plus will be the multiplier for facilitation only if n - b is positive, where n is the instantenous dopamine concentration in the volume transmitter. If n - b is negative, A_plus will be the multiplier for depression."    
    "A_minus", "real", "1.5", "Multiplier applied to weight changes caused by post-before-pre spike pairings. If b (dopamine baseline concentration) is zero, then A_minus is simply the multiplier for depression (as in the stdp_synapse model). If b is not zero, then A_minus will be the multiplier for depression only if n - b is positive, where n is the instantenous dopamine concentration in the volume transmitter. If n - b is negative, A_minus will be the multiplier for facilitation."



State variables
+++++++++++++++

.. csv-table::
    :header: "Name", "Physical unit", "Default value", "Description"
    :widths: auto

    
    "w", "real", "1.0", ""    
    "n", "real", "0.0", "Neuromodulator concentration"    
    "c", "real", "0.0", "Eligibility trace"    
    "pre_tr", "real", "0.0", ""    
    "post_tr", "real", "0.0", ""
Source code
+++++++++++

.. code-block:: nestml

   synapse neuromodulated_stdp:
     state:
       w real = 1.0
       n real = 0.0 # Neuromodulator concentration
       c real = 0.0 # Eligibility trace
       pre_tr real = 0.0
       post_tr real = 0.0
     end
     parameters:
       the_delay ms = 1ms # !!! cannot have a variable called "delay"
       tau_tr_pre ms = 20ms # STDP time constant for weight changes caused by pre-before-post spike pairings.
       tau_tr_post ms = 20ms # STDP time constant for weight changes caused by post-before-pre spike pairings.
       tau_c ms = 1000ms # Time constant of eligibility trace
       tau_n ms = 200ms # Time constant of dopaminergic trace
       b real = 0.0 # Dopaminergic baseline concentration
       Wmax real = 200.0 # Maximal synaptic weight
       Wmin real = 0.0 # Minimal synaptic weight
       A_plus real = 1.0 # Multiplier applied to weight changes caused by pre-before-post spike pairings. If b (dopamine baseline concentration) is zero, then A_plus is simply the multiplier for facilitation (as in the stdp_synapse model). If b is not zero, then A_plus will be the multiplier for facilitation only if n - b is positive, where n is the instantenous dopamine concentration in the volume transmitter. If n - b is negative, A_plus will be the multiplier for depression.
       A_minus real = 1.5 # Multiplier applied to weight changes caused by post-before-pre spike pairings. If b (dopamine baseline concentration) is zero, then A_minus is simply the multiplier for depression (as in the stdp_synapse model). If b is not zero, then A_minus will be the multiplier for depression only if n - b is positive, where n is the instantenous dopamine concentration in the volume transmitter. If n - b is negative, A_minus will be the multiplier for facilitation.
     end
     equations:
       pre_tr'=-pre_tr / tau_tr_pre
       post_tr'=-post_tr / tau_tr_post
     end

     internals:
       tau_s 1/ms = (tau_c + tau_n) / (tau_c * tau_n)
     end
     input:
       pre_spikes nS <-spike
       post_spikes nS <-spike
       mod_spikes real <-spike
     end

     output: spike

     onReceive(mod_spikes):
       n += 1.0 / tau_n
     end

     onReceive(post_spikes):
       post_tr += 1.0
       # facilitation
       c += A_plus * pre_tr
     end

     onReceive(pre_spikes):
       pre_tr += 1.0
       # depression
       c -= A_minus * post_tr
       # deliver spike to postsynaptic partner
       deliver_spike(w,the_delay)
     end

     # update from time t to t + resolution()
     update:
       # resolution() returns the timestep to be made (in units of time)
       # the sequence here matters: the update step for w requires the "old" values of c and n
       w -= c * (n / tau_s * expm1(-tau_s * resolution()) - b * tau_c * expm1(-resolution() / tau_c))
       c = c * exp(-resolution() / tau_c)
       n = n * exp(-resolution() / tau_n)
     end

   end



Characterisation
++++++++++++++++

.. include:: neuromodulated_stdp_characterisation.rst


.. footer::

   Generated at 2021-12-09 08:22:33.046196