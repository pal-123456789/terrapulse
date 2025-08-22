declare namespace Cesium {
    // Basic type definitions for Cesium
    export class Cartesian3 {
        static fromDegreesArray(coords: number[]): Cartesian3;
    }
    
    export class Cartesian2 {
        constructor(x: number, y: number);
    }
    
    export class Color {
        static RED: Color;
        static WHITE: Color;
        static BLACK: Color;
        withAlpha(alpha: number): Color;
    }
    
    export enum HeightReference {
        CLAMP_TO_GROUND
    }
    
    export enum LabelStyle {
        FILL_AND_OUTLINE
    }
    
    export class CustomDataSource {
        constructor(name: string);
        entities: EntityCollection;
    }
    
    export class EntityCollection {
        removeAll(): void;
        add(entity: Entity): Entity;
    }
    
    export interface Entity {
        id?: string;
        polygon?: PolygonGraphics;
        label?: LabelGraphics;
        properties?: any;
    }
    
    export interface PolygonGraphics {
        hierarchy: any;
        material: Color;
        outline: boolean;
        outlineColor: Color;
        outlineWidth: number;
        heightReference: HeightReference;
    }
    
    export interface LabelGraphics {
        text: string;
        font: string;
        pixelOffset: Cartesian2;
        fillColor: Color;
        outlineColor: Color;
        outlineWidth: number;
        style: LabelStyle;
        heightReference: HeightReference;
    }
    
    export class ScreenSpaceEventHandler {
        constructor(canvas: HTMLCanvasElement);
        setInputAction(action: Function, type: ScreenSpaceEventType): void;
    }
    
    export enum ScreenSpaceEventType {
        LEFT_CLICK
    }
    
    export function defined(obj: any): boolean;
}