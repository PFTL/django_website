<script>
    import { createEventDispatcher } from 'svelte';
import CustomButton from './CustomButton.svelte';

    const dispatch = createEventDispatcher();

    function sayHello() {
        dispatch('message', {
            text: 'Hello!'
        });
    }
</script>


<button on:click="{sayHello}">Click to say hello</button>

<CustomButton on:click="{sayHello}" />