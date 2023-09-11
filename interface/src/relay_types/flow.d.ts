type AnyData = { [key: string]: any }

export type Edge = {
    from: any,
    to: any,


} & AnyData

export type FlowEntry = {
    id: any,
    x: number,
    y: number,


} & AnyData

export type Flow = FlowEntry[]


export type Edges = Edge[];

export type DataTransfer = {
    flow: Flow,
    edges: Edges
}