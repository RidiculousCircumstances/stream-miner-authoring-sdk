# Stream Miner Go Authoring Types

Go is deferred for v1 of the authoring SDK split.

Python and JavaScript can provide useful types-only packages because their
authoring flows can depend on `.pyi` and `.d.ts` files without compiling a real
runtime module. Go parser code compiles against a module, so a package that is
"types only" would still need real exported declarations and would become part
of the build graph.

The current Go runtime SDK remains platform-owned and is not copied into this
authoring repository. A future Go authoring step should choose between:

- a small interface-only Go module that intentionally excludes runner/protocol
  implementation; or
- a published real Go SDK module with the runtime boundary explicitly owned by
  the platform contract.

Do not copy Agent, Control Plane, queue, framework, Proxy Manager, Stats Forge,
or database internals into a Go authoring package.
