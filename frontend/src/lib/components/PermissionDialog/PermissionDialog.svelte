<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	
	const dispatch = createEventDispatcher();
	
	let locationAllowed = false;
	let notificationsAllowed = false;
	
	function proceed() {
		dispatch('response', {
			location: locationAllowed,
			notifications: notificationsAllowed
		});
	}
</script>

<div class="permission-dialog-overlay">
	<div class="permission-dialog">
		<div class="dialog-header">
			<h2>Welcome to TerraPulse</h2>
			<p>To provide the best experience, we need your permission for:</p>
		</div>
		
		<div class="permission-options">
			<label class="permission-toggle">
				<input type="checkbox" bind:checked={locationAllowed} />
				<div class="toggle-content">
					<span class="icon">📍</span>
					<div class="text">
						<strong>Location Access</strong>
						<p>Show environmental data relevant to your area</p>
					</div>
				</div>
			</label>
			
			<label class="permission-toggle">
				<input type="checkbox" bind:checked={notificationsAllowed} />
				<div class="toggle-content">
					<span class="icon">🔔</span>
					<div class="text">
						<strong>Browser Notifications</strong>
						<p>Alert you about critical environmental events</p>
					</div>
				</div>
			</label>
		</div>
		
		<button on:click={proceed} class="proceed-btn">
			Continue to TerraPulse
		</button>
		
		<p class="privacy-note">
			Your privacy is important. We only use this data to personalize your experience.
			<a href="/privacy">Learn more</a>
		</p>
	</div>
</div>

<style>
	.permission-dialog-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.8);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 10000;
		backdrop-filter: blur(10px);
	}
	
	.permission-dialog {
		background: linear-gradient(135deg, #0c1d2f 0%, #16324c 100%);
		border-radius: 16px;
		padding: 2rem;
		max-width: 500px;
		width: 90%;
		color: white;
		box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}
	
	.dialog-header {
		text-align: center;
		margin-bottom: 2rem;
	}
	
	.dialog-header h2 {
		margin: 0 0 0.5rem 0;
		font-size: 1.8rem;
	}
	
	.dialog-header p {
		margin: 0;
		opacity: 0.8;
	}
	
	.permission-options {
		margin-bottom: 2rem;
	}
	
	.permission-toggle {
		display: flex;
		align-items: center;
		padding: 1rem;
		background: rgba(255, 255, 255, 0.05);
		border-radius: 12px;
		margin-bottom: 1rem;
		cursor: pointer;
		transition: background 0.2s ease;
	}
	
	.permission-toggle:hover {
		background: rgba(255, 255, 255, 0.1);
	}
	
	.permission-toggle input {
		margin-right: 1rem;
	}
	
	.toggle-content {
		display: flex;
		align-items: center;
		flex: 1;
	}
	
	.toggle-content .icon {
		font-size: 1.5rem;
		margin-right: 1rem;
	}
	
	.toggle-content .text strong {
		display: block;
		margin-bottom: 0.25rem;
	}
	
	.toggle-content .text p {
		margin: 0;
		font-size: 0.9rem;
		opacity: 0.7;
	}
	
	.proceed-btn {
		width: 100%;
		padding: 1rem;
		background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
		color: white;
		border: none;
		border-radius: 8px;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		transition: transform 0.2s ease, box-shadow 0.2s ease;
	}
	
	.proceed-btn:hover {
		transform: translateY(-2px);
		box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
	}
	
	.privacy-note {
		text-align: center;
		font-size: 0.85rem;
		margin-top: 1.5rem;
		opacity: 0.7;
	}
	
	.privacy-note a {
		color: #8b5cf6;
		text-decoration: none;
	}
</style>