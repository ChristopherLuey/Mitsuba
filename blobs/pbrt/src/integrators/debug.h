#ifndef PBRT_INTEGRATORS_DEBUG_H
#define PBRT_INTEGRATORS_DEBUG_H

#include "pbrt.h"
#include "integrator.h"
#include "scene.h"

typedef enum {
	DEBUG_U, DEBUG_V,
	DEBUG_GEOM_NORMAL_X,
	DEBUG_GEOM_NORMAL_Y,
	DEBUG_GEOM_NORMAL_Z,
	DEBUG_GEOM_POINT_X,
	DEBUG_GEOM_POINT_Y,
	DEBUG_GEOM_POINT_Z,
	DEBUG_SHAD_NORMAL_X,
	DEBUG_SHAD_NORMAL_Y,
	DEBUG_SHAD_NORMAL_Z,
	DEBUG_ONE,
	DEBUG_ZERO,
	DEBUG_HIT_SOMETHING
} DebugVariable;

class DebugIntegrator : public SurfaceIntegrator {
public:
	// DebugIntegrator Public Methods
	Spectrum Li(const Scene *scene, const Renderer *renderer, 
			const RayDifferential &ray, const Intersection &isect, 
			const Sample *sample, RNG &rng, MemoryArena &arena) const;
	DebugIntegrator( DebugVariable v[3] )
	{
		debug_variable[0] = v[0];
		debug_variable[1] = v[1];
		debug_variable[2] = v[2];
	}
private:
	DebugVariable debug_variable[3];
};


DebugIntegrator *CreateDebugIntegrator(const ParamSet &params);

#endif // PBRT_INTEGRATORS_DEBUG_H

