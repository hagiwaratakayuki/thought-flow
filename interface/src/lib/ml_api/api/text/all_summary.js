import { get } from "../client"
/**
 * @returns {Promise<import("$lib/ml_api/api_types/TextOverViews").TextOverViews>}
 */
export function all_summary() {
    return get('text/all_summary')

}
