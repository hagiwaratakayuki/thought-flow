import { GridInfo } from './flow';

export type NodeEventMessage = {
    gridInfo: GridInfo,
    mouseEvent: MouseEvent

}


export type NodeEvent = CustomEvent<NodeEventMessage>
