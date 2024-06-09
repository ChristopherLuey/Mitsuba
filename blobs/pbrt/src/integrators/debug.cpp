
/*
    pbrt source code Copyright(c) 1998-2007 Matt Pharr and Greg Humphreys.

    This file is part of pbrt.

    pbrt is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.  Note that the text contents of
    the book "Physically Based Rendering" are *not* licensed under the
    GNU GPL.

    pbrt is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

 */

// debug.cpp*
// Debug integrator by Greg Humphreys

// debug.cpp*

#include "integrators/debug.h"
#include "intersection.h"
#include "paramset.h"


Spectrum DebugIntegrator::Li(const Scene *scene,
        const Renderer *renderer, const RayDifferential &ray,
        const Intersection &isect, const Sample *sample, RNG &rng, MemoryArena &arena) const {

    BSDF *bsdf = isect.GetBSDF(ray, arena);

	float color[3] = {0,0,0};

	int i;
	for (i = 0 ; i < 3 ; i++)
	{
		if (debug_variable[i] == DEBUG_HIT_SOMETHING)
		{
			color[i] = 1;
		}
		else if (debug_variable[i] == DEBUG_ONE)
		{
			color[i] = 1;
		}
		else if (debug_variable[i] == DEBUG_ZERO)
		{
			color[i] = 0;
		}
		switch( debug_variable[i] )
		{
			case DEBUG_U:
				color[i] = fabsf(bsdf->dgShading.u);
				break;
			case DEBUG_V:
				color[i] = fabsf(bsdf->dgShading.v);
				break;
			case DEBUG_GEOM_NORMAL_X:
				color[i] = fabsf(bsdf->dgShading.nn.x + 1.0f)/2.0f;
				break;
			case DEBUG_GEOM_NORMAL_Y:
				color[i] = fabsf(bsdf->dgShading.nn.y + 1.0f)/2.0f;
				break;
			case DEBUG_GEOM_NORMAL_Z:
				color[i] = fabsf(bsdf->dgShading.nn.z + 1.0f)/2.0f;
				break;

			// Assumes world geometry is between -3.0 and 3.0
			case DEBUG_GEOM_POINT_X:
				color[i] = fabsf(bsdf->dgShading.p.x + 3.0f)/6.0f;
				break;
			case DEBUG_GEOM_POINT_Y:
				color[i] = fabsf(bsdf->dgShading.p.y + 3.0f)/6.0f;
				break;
			case DEBUG_GEOM_POINT_Z:
				color[i] = fabsf(bsdf->dgShading.p.z + 3.0f)/6.0f;
				break;
			default:
				break;
		}

	}

	return RGBSpectrum::FromRGB(color);
}

DebugIntegrator *CreateDebugIntegrator(const ParamSet &params) {
	
	string strs[3];
	strs[0] = params.FindOneString( "red", "u" );
	strs[1] = params.FindOneString( "green", "v" );
	strs[2] = params.FindOneString( "blue", "zero" );

	DebugVariable vars[3];

	int i;
	for (i = 0 ; i < 3 ; i++)
	{
		if (strs[i] == "u") { vars[i] = DEBUG_U; }
		else if (strs[i] == "v") { vars[i] = DEBUG_V; }
		else if (strs[i] == "nx") { vars[i] = DEBUG_GEOM_NORMAL_X; }
		else if (strs[i] == "ny") { vars[i] = DEBUG_GEOM_NORMAL_Y; }
		else if (strs[i] == "nz") { vars[i] = DEBUG_GEOM_NORMAL_Z; }
		else if (strs[i] == "px") { vars[i] = DEBUG_GEOM_POINT_X; }
		else if (strs[i] == "py") { vars[i] = DEBUG_GEOM_POINT_Y; }
		else if (strs[i] == "pz") { vars[i] = DEBUG_GEOM_POINT_Z; }
		else if (strs[i] == "snx") { vars[i] = DEBUG_SHAD_NORMAL_X; }
		else if (strs[i] == "sny") { vars[i] = DEBUG_SHAD_NORMAL_Y; }
		else if (strs[i] == "snz") { vars[i] = DEBUG_SHAD_NORMAL_Z; }
		else if (strs[i] == "hit") { vars[i] = DEBUG_HIT_SOMETHING; }
		else if (strs[i] == "zero") { vars[i] = DEBUG_ZERO; }
		else if (strs[i] == "one") { vars[i] = DEBUG_ONE; }
		else
		{
			Error( "Unknown debug type \"%s\", defaulting to zero.", strs[i].c_str() );
			vars[i] = DEBUG_ZERO;
		}
	}

	return new DebugIntegrator(vars);
}
