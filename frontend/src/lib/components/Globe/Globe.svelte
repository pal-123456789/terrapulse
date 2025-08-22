<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	// FIX: Import the entire Cesium library. 
	// Make sure you have installed the types with `npm install -D @types/cesium`
	import * as Cesium from 'cesium';
	import { predictions, generatePrediction } from '$lib/stores/predictions.store';
	import type { WildfirePredictionRequest, PredictionResponse, Event } from '$lib/types/prediction';
	import type { Unsubscriber } from 'svelte/store';

	// Declare component-level variables
	let viewer: Cesium.Viewer;
	let predictionDataSource: Cesium.CustomDataSource;
	let predictionEntities: Record<string, Cesium.Entity> = {};
	let cesiumContainer: HTMLDivElement; // This will be bound to the div element

	// This variable will hold the function to unsubscribe from the store
	let unsubscribePredictions: Unsubscriber;

	onMount(() => {
		// Initialize Cesium viewer inside onMount
		viewer = new Cesium.Viewer(cesiumContainer, {
			// It's good practice to disable UI elements you don't need
			animation: false,
			timeline: false,
			geocoder: false,
			homeButton: false,
			sceneModePicker: false,
			baseLayerPicker: false,
			navigationHelpButton: false,
			infoBox: false,
			selectionIndicator: false,
		});

		// Create a data source for our prediction entities
		predictionDataSource = new Cesium.CustomDataSource('Predictions');
		viewer.dataSources.add(predictionDataSource);

		// Subscribe to the predictions store and update the globe whenever the data changes
		unsubscribePredictions = predictions.subscribe(($predictions) => {
			if (viewer) { // Ensure viewer is initialized before trying to update
				updatePredictionEntities($predictions);
			}
		});

		setupEventSelection();

		// The onDestroy hook MUST be called within onMount or another setup lifecycle function.
		onDestroy(() => {
			// This code runs when the component is removed from the DOM
			if (unsubscribePredictions) {
				unsubscribePredictions(); // Important: prevent memory leaks
			}
			if (viewer && !viewer.isDestroyed()) {
				viewer.destroy(); // Clean up the Cesium viewer instance
			}
		});
	});

	// Update prediction entities on the globe
	function updatePredictionEntities(allPredictions: Record<string, PredictionResponse>) {
		if (!predictionDataSource) return; // Guard clause to prevent errors

		predictionDataSource.entities.removeAll();
		predictionEntities = {};

		Object.values(allPredictions).forEach(prediction => {
			if (prediction.model_type === 'wildfire' && prediction.result?.predicted_perimeter) {
				try {
					const perimeter = prediction.result.predicted_perimeter;
					
					if (!perimeter.coordinates || perimeter.coordinates.length === 0) {
						console.warn('Skipping prediction with invalid perimeter:', prediction);
						return;
					}

					const entity = predictionDataSource.entities.add({
						id: prediction.prediction_id,
						polygon: {
							hierarchy: Cesium.Cartesian3.fromDegreesArray(
								perimeter.coordinates[0].flat()
							),
							material: Cesium.Color.RED.withAlpha(0.3),
							outline: true,
							outlineColor: Cesium.Color.RED,
							outlineWidth: 2,
							heightReference: Cesium.HeightReference.CLAMP_TO_GROUND,
						},
						properties: {
							// Store data directly on the entity for later retrieval on click
							prediction_id: prediction.prediction_id,
							confidence: prediction.confidence,
						}
					});
					predictionEntities[prediction.prediction_id] = entity;
				} catch (error) {
					console.error('Error adding prediction entity:', error, prediction);
				}
			}
		});
	}

	// Function to generate a prediction for an event
	async function generateEventPrediction(event: Event) {
		try {
			const request: WildfirePredictionRequest = {
				event_id: event.id,
				wind_speed: 15,
				wind_direction: 270,
				forecast_hours: 6
			};
			await generatePrediction(request);
		} catch (error) {
			console.error('Error generating prediction:', error);
		}
	}

	// Sets up the click handler on the Cesium canvas
	function setupEventSelection() {
		const handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
		handler.setInputAction((movement: { position: Cesium.Cartesian2 }) => {
			const pickedObject = viewer.scene.pick(movement.position);
			if (Cesium.defined(pickedObject) && pickedObject.id && pickedObject.id.properties) {
				const eventId = pickedObject.id.id;
				const eventProps = pickedObject.id.properties;
				
				if (eventProps.category?.getValue(viewer.clock.currentTime) === 'wildfires') {
					showPredictionOptions(eventId, eventProps);
				}
			}
		}, Cesium.ScreenSpaceEventType.LEFT_CLICK);
	}

	function showPredictionOptions(eventId: string, eventProps: any) {
		const currentTime = viewer.clock.currentTime;
		generateEventPrediction({
			id: eventId,
			title: eventProps.title?.getValue(currentTime) || 'Unknown Event',
			category_id: eventProps.category?.getValue(currentTime) || 'unknown',
		});
	}

	function clearPredictions() {
		if (predictionDataSource) {
			predictionDataSource.entities.removeAll();
		}
		predictionEntities = {};
		predictions.set({}); // Also clear the store
	}
</script>

<!-- The div for the Cesium container. `bind:this` gives us a reference to the DOM element. -->
<div id="cesiumContainer" bind:this={cesiumContainer}></div>

<!-- UI Controls -->
<div class="layer-controls">
	<h3>Predictions</h3>
	<div class="prediction-controls">
		<button on:click={clearPredictions}>Clear Predictions</button>
	</div>
</div>

<style>
	#cesiumContainer {
		width: 100%;
		height: 100%;
		position: absolute;
		top: 0;
		left: 0;
	}
	.layer-controls {
		position: absolute;
		top: 10px;
		right: 10px;
		background: rgba(42, 42, 42, 0.8);
		padding: 10px;
		border-radius: 8px;
		color: white;
		z-index: 10;
	}
	.prediction-controls {
		margin-top: 10px;
	}
	.prediction-controls button {
		width: 100%;
		padding: 8px;
		background: rgba(255, 107, 107, 0.2);
		color: white;
		border: 1px solid rgba(255, 107, 107, 0.5);
		border-radius: 4px;
		cursor: pointer;
		transition: background-color 0.2s;
	}
	.prediction-controls button:hover {
		background: rgba(255, 107, 107, 0.4);
	}
</style>
