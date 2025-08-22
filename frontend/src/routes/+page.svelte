<script lang="ts">
	import Globe from '$lib/components/Globe/Globe.svelte';
	import PermissionDialog from '$lib/components/PermissionDialog/PermissionDialog.svelte';
	
	let permissionsGranted = false;
	let locationAccess = false;
	let notificationAccess = false;
	
	function handlePermissions(e: CustomEvent<{ location: boolean; notifications: boolean }>) {
		permissionsGranted = true;
		locationAccess = e.detail.location;
		notificationAccess = e.detail.notifications;
		
		console.log('Permissions granted:', e.detail);
	}
</script>

{#if !permissionsGranted}
	<PermissionDialog on:response={handlePermissions} />
{:else}
	<div class="dashboard">
		<header class="app-header">
			<h1>🌍 TerraPulse</h1>
			<p>Real-time Planetary Health Monitoring</p>
		</header>
		
		<main class="main-content">
			<Globe />
		</main>
		
		<aside class="sidebar">
			<div class="sidebar-section">
				<h3>Event Timeline</h3>
				<div class="event-list">
					<div class="event-item">
						<div class="event-type fire">🔥</div>
						<div class="event-details">
							<strong>Wildfire detected</strong>
							<p>Northern California • 15 min ago</p>
						</div>
					</div>
					<div class="event-item">
						<div class="event-type storm">🌀</div>
						<div class="event-details">
							<strong>Tropical storm forming</strong>
							<p>Eastern Pacific • 2 hours ago</p>
						</div>
					</div>
				</div>
			</div>
		</aside>
	</div>
{/if}

<style>
	.dashboard {
		display: grid;
		grid-template-columns: 1fr 350px;
		grid-template-rows: auto 1fr;
		height: 100vh;
		grid-template-areas:
			"header header"
			"main sidebar";
	}
	
	.app-header {
		grid-area: header;
		background: rgba(0, 0, 0, 0.8);
		color: white;
		padding: 1rem 2rem;
		backdrop-filter: blur(10px);
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	}
	
	.app-header h1 {
		margin: 0;
		font-size: 1.8rem;
	}
	
	.app-header p {
		margin: 0;
		opacity: 0.8;
	}
	
	.main-content {
		grid-area: main;
		position: relative;
	}
	
	.sidebar {
		grid-area: sidebar;
		background: rgba(0, 0, 0, 0.7);
		color: white;
		padding: 1rem;
		overflow-y: auto;
		backdrop-filter: blur(10px);
		border-left: 1px solid rgba(255, 255, 255, 0.1);
	}
	
	.sidebar-section {
		margin-bottom: 2rem;
	}
	
	.sidebar-section h3 {
		margin-top: 0;
		border-bottom: 1px solid rgba(255, 255, 255, 0.2);
		padding-bottom: 0.5rem;
	}
	
	.event-item {
		display: flex;
		margin-bottom: 1rem;
		padding: 0.75rem;
		background: rgba(255, 255, 255, 0.05);
		border-radius: 6px;
	}
	
	.event-type {
		font-size: 1.5rem;
		margin-right: 0.75rem;
	}
	
	.event-details {
		flex: 1;
	}
	
	.event-details strong {
		display: block;
		margin-bottom: 0.25rem;
	}
	
	.event-details p {
		margin: 0;
		font-size: 0.85rem;
		opacity: 0.7;
	}
</style>