<script>
	import {spring} from 'svelte/motion'

	let coords = spring({x: 10, y:10});
	let size = spring(10);
</script>

<style global lang="postcss">

  /* only apply purgecss on utilities, per Tailwind docs */
  /* purgecss start ignore */
  @tailwind base;
  @tailwind components;
  /* purgecss end ignore */

  @tailwind utilities;

  a.wikilink {
    @apply no-underline shadow-wikilink transition duration-300 ease-in-out;
}
  a.wikilink:hover {
    @apply shadow-wikihover;
}
	svg { width: 100%; height: 100%; margin: -8px; }
	circle { fill: #ff3e00 }
</style>

<div class="bg-gray-300">
	<label>
		<h3>stiffness ({coords.stiffness})</h3>
		<input bind:value={coords.stiffness} type="range" min="0" max="1" step="0.01">
	</label>

	<label>
		<h3>damping ({coords.damping})</h3>
		<input bind:value={coords.damping} type="range" min="0" max="1" step="0.01">
	</label>
</div>

<svg
	on:mousemove="{e => coords.set({ x: e.clientX, y: e.clientY })}"
	on:mousedown="{() => size.set(30)}"
	on:mouseup="{() => size.set(10)}"
>
	<circle cx={$coords.x} cy={$coords.y} r={$size}/>
</svg>