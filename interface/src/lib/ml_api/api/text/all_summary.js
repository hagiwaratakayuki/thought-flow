import { get } from "../client"
/**
 * @returns {Promise<false | import("src/lib/ml_api/api_types/TextOverViews").TextOverViews>}
 */
export function all_summary() {
    return get('/all_summery')

}
