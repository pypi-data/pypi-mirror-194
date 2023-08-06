#pragma once

#include "akida/dense.h"

#include "infra/exports.h"

namespace akida {

AKIDASHAREDLIB_EXPORT void check_weights_range(const akida::Dense& weights);

}  // namespace akida
