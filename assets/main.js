import App from './App.svelte';

let target = document.querySelector('#newsletter');

const app = new App({
	target: document.body,
});

export default app;