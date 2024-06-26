variable "ANALYTICS_BASE_URL" {
  description = "value"
  type        = string
}

/* ------------------------ Analytics and Sourcing Auth Flow ------------------------ */

variable "PARMA_SHARED_SECRET_KEY" {
  description = "Shared secret key for the analytics and sourcing auth flow"
  type        = string
  sensitive   = true
}


/* ----------------------------------- Crunchbase ----------------------------------- */

variable "APIFY_ACTOR_ID" {
  description = "Apify actor ID"
  type        = string
  sensitive   = false
}

variable "APIFY_API_KEY" {
  description = "Apify API key"
  type        = string
  sensitive   = true
}
