<script>
    import Inner from './Inner.svelte';

    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    function forward(event) {
        event.detail.text += 'a';
        dispatch('message', event.detail);
    }
</script>

<Inner on:message={forward}></Inner>